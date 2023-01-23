import bpy
import os
import json
from ..utilities.general import preset_path_get

class Paladin_OT_ExportFbx(bpy.types.Operator):
    bl_idname = "paladin.exportfbx"
    bl_label = "Export FBX"

    def execute(self, context):
        export_data = context.scene.exporter
        sets = export_data.sets
        preset_path = preset_path_get()
        old_selected = context.selected_objects
        old_active = context.view_layer.objects.active
        old_mode = context.object.mode
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        for set in sets:
            if set.set_include == False:
                continue
            preset_setting = os.path.join(preset_path, set.set_preset)
            with open(preset_setting, 'r') as preset_setting:
                self.settings = json.load(preset_setting)

            for item in set.items:
                if item.item_include == False:
                    continue
                collection = bpy.data.collections[item.item_name]
                if collection is None:
                    print(f"collection not found: '{item.item_name}'")
                    continue
                print (set.set_preset)
                print (item.item_name)
        
        
        # Resetting selected/active objects and mode:
        bpy.ops.object.select_all(action='DESELECT')
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
