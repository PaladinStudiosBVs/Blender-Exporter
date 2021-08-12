import bpy
import uuid

class Paladin_OT_RemoveExportItem(bpy.types.Operator):
    bl_idname = "paladin.export_items_list_remove_item"
    bl_label = "Remove"

    @classmethod
    def poll(cls, context):
        return context.scene.ExportItemsList

    def execute(self, context):
        itemsList = context.scene.ExportItemsList
        index = context.scene.ExportItemsIndex

        itemsList.remove(index)
        context.scene.ExportItemsIndex = 0 ## min(max(0, index - 1), len(itemsList) - 1)
        return{'FINISHED'}

classes = (Paladin_OT_RemoveExportItem,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
