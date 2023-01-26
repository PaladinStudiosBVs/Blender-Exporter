import bpy, os, sys, json
from bpy.props import BoolProperty
from ..utilities.general import preset_path_get, is_collection_valid, has_export_sets, has_sets_include
from ..utilities.general import included_sets_has_item, get_event_modifiers, get_export_path
from ..utilities.exporters import export_fbx
from ..data.items import keys

class Paladin_OT_ExportFbx(bpy.types.Operator):
    bl_idname = "paladin.exportfbx"
    bl_label = "Export FBX"
    
    export_selected: BoolProperty(name="Export Selected", default=False)
    
    @classmethod
    def poll(cls, context):
        if not bpy.data.is_saved:
            return False
        if not has_export_sets():
            return False
        if not has_sets_include():
            return False
        if not included_sets_has_item():
            return False   
        return True
    
    @classmethod
    def description(cls, context, event):
        key_press = keys['WINDOWS']
        if sys.platform.startswith('darwin'):
            key_press = keys['MAC']
        if not bpy.data.is_saved:
            return "Save the file before Exporting"
        if not has_export_sets():
            return "Create at least one Export Set"
        if not has_sets_include():
            return "Enable at least one Export Set"
        if not included_sets_has_item():
            return "Add items to the enabled Export Set(s)"
        return f"Export items from export sets\n{key_press[2]}   ▸   Export Selected"

    def invoke(self, context, event):
        self.ctrl, self.alt, self.shift = get_event_modifiers(event)
        return self.execute(context)

    def execute(self, context):
        object_types = ('MESH','EMPTY','ARMATURE')
        export_sets = context.scene.exporter.sets
        preset_path = preset_path_get()
        old_selected = context.selected_objects
        old_active = context.view_layer.objects.active if len(old_selected) > 0 else None
        old_mode = context.object.mode if old_active else None
        exported_objects = []
        
        for export_set in export_sets:
            if export_set.include == False:
                continue
            
            self.settings = json.load(open(os.path.join(preset_path, export_set.preset), 'r'))
            prefix = export_set.prefix
            suffix = export_set.suffix
            
            for export_item in export_set.items:
                item_name = export_item.name
                if export_item.include == False:
                    continue
                if not is_collection_valid(item_name):
                    print(f"Collection not found: '{item_name}'")
                    continue
                
                collection = bpy.data.collections[item_name]
                export_objects = []
                
                # With export item use collection:
                if export_item.use_collection == True:
                    v_collection = bpy.context.view_layer.layer_collection.children[item_name]
                    export_objects_collection = []
                    if collection.hide_viewport or v_collection.exclude:
                        continue
                    for obj in collection.objects:
                        if obj.parent == None and obj.type in object_types and obj.visible_get() == True:
                            export_objects_collection.append(obj)
                    if len(export_objects_collection) > 0:
                        filename = (prefix)+(item_name)+(suffix)+".fbx"
                        export_path = get_export_path(export_set, export_item, filename)
                        exported_objects.append(filename) 
                        
                        for obj in export_objects_collection:
                            obj.select_set(True)
                            context.view_layer.objects.active = obj
                        export_fbx(self, export_path)
                
                # With export selected:
                if self.export_selected == True or self.alt:
                    for obj in collection.objects:
                        # Selecting parent if selected object is nested:
                        if not obj.parent == None and obj.type in object_types and obj.select_get() == True and obj.parent.visible_get() == True:
                            obj = obj.parent
                            if obj in export_objects:
                                continue
                            export_objects.append(obj)
                        # Selecting selected parent objects:
                        if obj.parent == None and obj.type in object_types and obj.select_get() == True and obj.visible_get() == True :
                            export_objects.append(obj)
                            continue

                # Default export behavior:
                else:                    
                    for obj in collection.objects:
                        if obj.parent == None and obj.type in object_types and obj.visible_get() == True:
                            export_objects.append(obj)
                        continue
                
                # Exporting if use collection as object is disabled:          
                if export_item.use_collection == False and len(export_objects) > 0:
                    for obj in export_objects:
                        filename = (prefix)+(obj.name)+(suffix)+".fbx"
                        export_path = get_export_path(export_set, export_item, filename)
                        exported_objects.append(filename)

                        bpy.ops.object.mode_set(mode='OBJECT')
                        bpy.ops.object.select_all(action='DESELECT')
                        obj.select_set(True)
                        context.view_layer.objects.active = obj
                        old_location = obj.location.copy()
                        if not export_item.use_origin:
                            obj.location = (0,0,0)
                        export_fbx(self, export_path)
                        obj.location = old_location
                        
                # Selecting old object(s) to be able to check for selected objects next loop:
                if len(old_selected) > 0:
                    bpy.ops.object.select_all(action='DESELECT')
                    for obj in old_selected:
                        obj.select_set(True)
        
        # Reporting number of exported objects:
        length = len(exported_objects)
        if length == 0:
            self.report({'ERROR'},"No objects were exported")
        elif length == 1:
            self.report({'INFO'},"One object was exported")
        else:
            self.report({'INFO'},f"{length} objects were exported")

        # Resetting selected/active objects and mode:
        bpy.ops.object.select_all(action='DESELECT')
        if len(old_selected) > 0:
            for obj in old_selected:
                obj.select_set(True)
            context.view_layer.objects.active = old_active
            if not old_active == None:
                bpy.ops.object.mode_set(mode=old_mode)

        return {'FINISHED'}

classes = (Paladin_OT_ExportFbx,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
