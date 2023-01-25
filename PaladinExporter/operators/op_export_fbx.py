import bpy, os, sys, json
from bpy.props import BoolProperty
from ..utilities.general import preset_path_get, is_collection_valid, has_export_sets, has_sets_include, included_sets_has_item, get_event_modifiers
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
        export_data = context.scene.exporter
        export_sets = export_data.sets
        preset_path = preset_path_get()
        old_selected = context.selected_objects
        exported_objects = []
        
        if len(old_selected) > 0:
            old_active = context.view_layer.objects.active
            old_mode = context.object.mode

        for export_set in export_sets:
            if export_set.set_include == False:
                continue
            with open(os.path.join(preset_path, export_set.set_preset), 'r') as preset_setting:
                self.settings = json.load(preset_setting)

            for export_item in export_set.items:
                if export_item.item_include == False:
                    continue
                if not is_collection_valid(export_item.item_name):
                    print(f"Collection not found: '{export_item.item_name}'")
                    continue
                collection = bpy.data.collections[export_item.item_name]

                # Checking which objects to export for Export Set:
                export_objects = []
                export_objects_selected = []
                object_types = ('MESH','EMPTY','ARMATURE')
                
                if export_item.item_use_collection == True:
                    if collection.hide_viewport:
                        continue
                    collection_objects = []
                    for obj in collection.objects:
                        if obj.parent == None and obj.type in object_types and obj.visible_get() == True:
                            collection_objects.append(obj)
                    if len(collection_objects) <1:
                        continue    
                    for obj in collection_objects:
                        obj.select_set(True)

                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.select_all(action='DESELECT')
                    filename = f"{export_set.set_prefix}{collection.name}{export_set.set_suffix}.fbx"
                    export_path = os.path.join(os.path.dirname(bpy.data.filepath), filename)
                    if export_item.item_use_path and not export_item.item_path == "":
                        export_path = os.path.join(export_item.item_path, filename)
                    elif not export_set.set_path == "":
                        export_path = os.path.join(export_set.set_path, filename)
                    exported_objects.append(filename)
                    export_fbx(self, export_path)
                    continue
                else:
                    for obj in collection.objects:
                        if obj.parent == None and obj.type in object_types and obj.visible_get() == True:
                            export_objects.append(obj)
                        if not obj.parent == None and obj.type in object_types and obj.select_get() == True and obj.parent.visible_get() == True:
                            obj = obj.parent
                            if obj in export_objects_selected:
                                continue
                            export_objects_selected.append(obj)
                        if obj.parent == None and obj.type in object_types and obj.select_get() == True and obj.visible_get() == True :
                            export_objects_selected.append(obj)
                    if len(export_objects) == 0:
                        continue

                    # Parent objects in the collection will now be setup for export:
                    old_mode = context.object.mode
                    export_objects
                    
                    # Checking if we are exporting selected:
                    if self.export_selected == True or self.alt:
                        export_objects = export_objects_selected

                    for obj in export_objects:
                        bpy.ops.object.select_all(action='DESELECT')
                        obj.select_set(True)
                        context.view_layer.objects.active = obj
                        bpy.ops.object.mode_set(mode='OBJECT')
                        bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
                        old_location = obj.location.copy()
                        if not export_item.item_use_origin:
                            obj.location = (0,0,0)
                        # Defining file name and export location:
                        filename = f"{export_set.set_prefix}{obj.name}{export_set.set_suffix}.fbx"
                        export_path = os.path.join(os.path.dirname(bpy.data.filepath), filename)
                        if export_item.item_use_path and not export_item.item_path == "":
                            export_path = os.path.join(export_item.item_path, filename)
                        elif not export_set.set_path == "":
                            export_path = os.path.join(export_set.set_path, filename)
                        # Appending all exported objects to check number of exported objects:
                        exported_objects.append(filename)
                        # Exporting:
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
            bpy.ops.object.mode_set(mode=old_mode)

        print("Done")

        return {'FINISHED'}

classes = (Paladin_OT_ExportFbx,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
