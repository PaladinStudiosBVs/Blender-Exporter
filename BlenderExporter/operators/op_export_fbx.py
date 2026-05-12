import bpy, os, sys, json
from bpy.props import BoolProperty
from ..utilities.general import preset_path_get, is_collection_valid, has_sets_include
from ..utilities.general import included_sets_has_item, get_event_modifiers, get_export_path, exportable, exportable_selected, exportable_selected_nested, exportable_all, exportable_selected_all, exportable_selected_nested_all
from ..utilities.exporters import export_fbx
from ..utilities.general import get_collection_name
from ..data.items import keys

class Paladin_OT_ExportFbx(bpy.types.Operator):
    bl_idname = "paladin.exportfbx"
    bl_label = "Export FBX"
    
    export_selected: BoolProperty(name="Export Selected", default=False)
    
    @classmethod
    def poll(cls, context):
        export_sets = context.scene.exporter.sets

        if not bpy.data.is_saved:
            return False
        if not export_sets:
            return False
        if not has_sets_include(export_sets):
            return False
        if not included_sets_has_item(export_sets):
            return False   
        return True
    
    @classmethod
    def description(cls, context, event):
        export_sets = context.scene.exporter.sets

        key_press = keys['WINDOWS']
        if sys.platform.startswith('darwin'):
            key_press = keys['MAC']
        if not bpy.data.is_saved:
            return "Save the file before Exporting"
        if not export_sets:
            return "Create at least one Export Set"
        if not has_sets_include(export_sets):
            return "Enable at least one Export Set"
        if not included_sets_has_item(export_sets):
            return "Add items to the enabled Export Set(s)"
        return f"Export items from export sets\n{key_press[2]}   ▸   Export Selected"

    def invoke(self, context, event):
        self.ctrl, self.alt, self.shift = get_event_modifiers(event)
        return self.execute(context)

    def execute(self, context):
        if not hasattr(self, 'alt'):
            self.ctrl = self.alt = self.shift = False
        export_sets = context.scene.exporter.sets
        preset_path = preset_path_get()

        # Capture the original state before any changes
        current_active = context.view_layer.objects.active
        current_mode = current_active.mode if current_active else 'OBJECT'

        # Switch to Object Mode if needed (export requires Object Mode context)
        if current_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Capture the selection state now that we are in Object Mode
        old_selected = list(context.selected_objects)
        old_active = context.view_layer.objects.active if old_selected else None
        
        exported_objects = []
        
        for i, export_set in enumerate(export_sets):
            if not export_set.include:
                self.report({'INFO'},(f"Skipped 'Export Set {i + 1}'\n"))
                continue
            self.report({'INFO'},(f"Exported 'Export Set {i + 1}'\n"))
            self.settings = json.load(open(os.path.join(preset_path, export_set.preset), 'r'))
            prefix = export_set.prefix
            suffix = export_set.suffix
            
            for export_item in export_set.items:
                item_uuid = export_item.uuid
                if not export_item.include:
                    continue
                if not is_collection_valid(item_uuid):
                    continue
                    
                item_name = get_collection_name(item_uuid)
                coll = bpy.data.collections[item_name]
                v_coll = bpy.context.view_layer.layer_collection.children[item_name]
                coll_objects = coll.objects
                is_export_selected = (self.alt or self.export_selected)
                is_export_selected_valid = any(obj.select_get() for obj in coll.objects)
                export_objects = []

                # Select filter functions based on include_hidden toggle:
                if export_item.include_hidden:
                    filter_fn = exportable_all
                    filter_selected_fn = exportable_selected_all
                    filter_selected_nested_fn = exportable_selected_nested_all
                else:
                    filter_fn = exportable
                    filter_selected_fn = exportable_selected
                    filter_selected_nested_fn = exportable_selected_nested

                # With export item use collection:
                if export_item.use_collection:
                    if coll.hide_viewport or v_coll.exclude:
                        continue
                    if is_export_selected:
                        if is_export_selected_valid:
                            export_objects = [obj for obj in coll_objects if filter_fn(obj)]
                    else:
                        export_objects = [obj for obj in coll_objects if filter_fn(obj)]
                    
                    # Exporting:
                    if export_objects:
                        
                        # Temporarily unhide objects for export when visible_only is off:
                        hidden_objects = []
                        if export_item.include_hidden:
                            for obj in coll_objects:
                                if obj.hide_get():
                                    obj.hide_set(False)
                                    hidden_objects.append(obj)
                        
                        filename = (prefix)+(item_name)+(suffix)+".fbx"
                        export_path = get_export_path(export_set, export_item, filename)
                        exported_objects.append(filename)
                        bpy.ops.object.select_all(action='DESELECT')
                        for obj in export_objects:
                            obj.select_set(True)
                            context.view_layer.objects.active = obj
                            bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
                        export_fbx(self, export_path)
                        self.report({'INFO'},f"Exported {prefix}{item_name}{suffix}")
                        
                        # Restore hidden state:
                        for obj in hidden_objects:
                            obj.hide_set(True)
                else:
                    if is_export_selected:
                        if is_export_selected_valid:
                            export_objects_nested = set(obj.parent for obj in coll_objects if filter_selected_nested_fn(obj))
                            export_objects = set(obj for obj in coll_objects if filter_selected_fn(obj))
                            export_objects = export_objects.union(export_objects_nested)
                    else:
                        export_objects = [obj for obj in coll_objects if filter_fn(obj)]

                    # Exporting:
                    if export_objects:
                        
                        # Temporarily unhide objects for export when visible_only is off:
                        hidden_objects = []
                        if export_item.include_hidden:
                            for obj in coll_objects:
                                if obj.hide_get():
                                    obj.hide_set(False)
                                    hidden_objects.append(obj)

                        for obj in export_objects:
                            filename = (prefix)+(obj.name)+(suffix)+".fbx"
                            export_path = get_export_path(export_set, export_item, filename)
                            exported_objects.append(filename)
                            
                            bpy.ops.object.select_all(action='DESELECT')
                            obj.select_set(True)
                            context.view_layer.objects.active = obj
                            bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
                            old_location = obj.location.copy()
                            if not export_item.use_origin:
                                obj.location = (0,0,0)
                            export_fbx(self, export_path)
                            self.report({'INFO'},f"Exported '{prefix}{obj.name}{suffix}'")
                            obj.location = old_location
                        
                        # Restore hidden state:
                        for obj in hidden_objects:
                            obj.hide_set(True)
                        
                # Restore selection to check for selected objects next loop:
                bpy.ops.object.select_all(action='DESELECT')
                for obj in old_selected:
                    obj.select_set(True)
                if old_active:
                    context.view_layer.objects.active = old_active

        # Restore the original selection and mode
        bpy.ops.object.select_all(action='DESELECT')
        for obj in old_selected:
            obj.select_set(True)
        if current_active:
            context.view_layer.objects.active = current_active
            if current_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=current_mode)
        
        # Reporting number of exported objects:
        length = len(exported_objects)
        if length == 0:
            self.report({'ERROR'},"No objects were exported")
        elif length == 1:
            self.report({'INFO'},"One object was exported")
        else:
            self.report({'INFO'},f"{length} objects were exported")

        return {'FINISHED'}

classes = (Paladin_OT_ExportFbx,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
