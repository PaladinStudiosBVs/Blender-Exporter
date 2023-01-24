import bpy
import os
import json
from bpy.props import BoolProperty
from ..utilities.general import preset_path_get, is_collection_valid, has_export_sets, has_sets_include, included_sets_has_item
from ..utilities.exporters import export_fbx

export_selected: BoolProperty(name="Export Selected", default=False)

class Paladin_OT_ExportFbx(bpy.types.Operator):
    bl_idname = "paladin.exportfbx"
    bl_label = "Export FBX"
    bl_options = {'UNDO'}

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
        if not bpy.data.is_saved:
            return "Save the file before Exporting"
        if not has_export_sets():
            return "Create at least one Export Set"
        if not has_sets_include():
            return "Enable at least one Export Set"
        if not included_sets_has_item():
            return "Add items to the enabled Export Set(s)"
        return "Export items from the export sets"

    def execute(self, context):
        export_data = context.scene.exporter
        export_sets = export_data.sets
        preset_path = preset_path_get()
        old_selected = context.selected_objects
        
        if len(old_selected) > 0:
            old_active = context.view_layer.objects.active
            old_mode = context.object.mode

        
        
        for export_set in export_sets:
            if export_set.set_include == False:
                continue
            with open(os.path.join(preset_path, export_set.set_preset), 'r') as preset_setting:
                self.settings = json.load(preset_setting)

            for item in export_set.items:
                if item.item_include == False:
                    continue
                if not is_collection_valid(item.item_name):
                    print(f"Collection not found: '{item.item_name}'")
                    continue
                collection = bpy.data.collections[item.item_name]
                
                # Checking which objects to export for this collection:
                parent_objects = []
                parent_objects_selected = []
                object_types = ('MESH','EMPTY','ARMATURE')

                for obj in collection.objects:
                    if obj.parent == None and obj.type in object_types and obj.visible_get() == True:
                        parent_objects.append(obj)
                
                    if not obj.parent == None and obj.type in object_types and obj.select_get() == True and obj.parent.visible_get() == True:
                        obj = obj.parent
                        parent_objects_selected.append(obj)
                
                    if obj.parent == None and obj.type in object_types and obj.select_get() == True and obj.visible_get() == True :
                        parent_objects_selected.append(obj)
                
                # If there are no objects in the list it will continue with other collections:
                if len(parent_objects) == 0:
                    continue

                for obj in parent_objects_selected:
                    print(obj.name)
                
                # Parent objects in the collection will now be setup for export:
                old_mode = context.object.mode
                bpy.ops.object.mode_set(mode='OBJECT')
                
                export_objects = parent_objects
                if self.export_selected:
                    export_objects = parent_objects_selected
                
                for obj in export_objects:
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(True)
                    context.view_layer.objects.active = obj
                    bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')
                    old_location = obj.location.copy()
                    if not item.item_use_origin:
                        obj.location = (0,0,0)
                    
                    # Defining file name and export location:
                    filename = f"{export_set.set_prefix}{obj.name}{export_set.set_suffix}.fbx"
                    export_path = os.path.join(os.path.dirname(bpy.data.filepath), filename)
                    if item.item_use_path and not item.item_path == "":
                        export_path = os.path.join(item.item_path, filename)
                    elif not export_set.set_path == "":
                        export_path = os.path.join(export_set.set_path, filename)
                    
                    # Exporting using fbx:
                    export_fbx(self, export_path)
                    # Resetting object position:
                    
                    obj.location = old_location
        
        # Reporting number of exported objects:
        length = len(export_objects)
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

        return {'FINISHED'}

classes = (Paladin_OT_ExportFbx,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
