import bpy

class Paladin_OT_AddExportItem(bpy.types.Operator):
    bl_idname = "paladin.export_items_list_new_item"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        collection = context.collection

        if collection is None:
            return False

        for item in context.scene.ExportItemsList:
            if item.collection_name == collection.name:
                return False

        return context.collection

    def execute(self, context):
        collection = context.collection
        item = context.scene.ExportItemsList.add()
        item.collection_name = collection.name
        return{'FINISHED'}

classes = (Paladin_OT_AddExportItem,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
