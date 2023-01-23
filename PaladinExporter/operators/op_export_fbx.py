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
        '''
        for set in sets:
            for i, item in enumerate(set):
                print (item.collection_name)

            ##item_values = set.items.values()

         '''     
        return {'FINISHED'}

classes = (Paladin_OT_ExportFbx,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
