import bpy
from bpy.props import EnumProperty

class Paladin_OT_ExportItemRemove(bpy.types.Operator):
    bl_idname = "paladin.export_item_remove"
    bl_label = "Remove"

    @classmethod
    def poll(cls, context):
        export_data = context.scene.exporter
        return export_data.items_list

    @classmethod
    def description(cls, context, event):
        export_data = context.scene.exporter
        if not export_data.items_list:
            return "No Export Collection to Remove"
        return "Remove selected Export Collection from export list"

    def execute(self, context):
        export_data = context.scene.exporter
        items = export_data.items_list
        index = export_data.items_index

        items.remove(index)
        # Selects item above index when it is removed:
        export_data.items_index = min(max(0, index - 1), len(items) - 1)
        return{'FINISHED'}


class Paladin_OT_ExportItemAdd(bpy.types.Operator):
    bl_idname = "paladin.export_items_add"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        collection = context.collection
        export_data = context.scene.exporter
        items = export_data.items_list

        if collection is None:
            return False
        for item in items:
            if item.collection_name == collection.name:
                return False
        return context.collection
    
    @classmethod
    def description(cls, context, event):
        collection = context.collection
        export_data = context.scene.exporter
        items = export_data.items_list

        if collection is None:
            return "There are no collections in the scene"
        for item in items:
            if item.collection_name == collection.name:
                return f"Collection '{collection.name}' is already in the export list"
        return f"Adds Collection '{collection.name}' to the export list"

    def execute(self, context):
        collection = context.collection
        export_data = context.scene.exporter
        items = export_data.items_list

        item = items.add()
        item.collection_name = collection.name
        
        export_data.export_item_index = len(items)-1
        return{'FINISHED'}

class Paladin_OT_ExportItemMove(bpy.types.Operator):
    bl_idname = "paladin.export_item_move"
    bl_label = "Move"

    direction: EnumProperty(
        items=[
            ('UP', 'Up',""),
            ('DOWN', 'Down',"")]
            )

    @classmethod
    def description(cls, context, event):        
        return "Move Export Collection up or down"
    
    @classmethod
    def poll(cls, context):
        export_data = context.scene.exporter
        items = export_data.items_list

        if len(items) <= 1:
            return False
        return True
    
    def execute(self, context):
        export_data = context.scene.exporter
        items = export_data.items_list
        index = export_data.items_index

        if self.direction == "UP":
            next_index = max(index -1, 0)
        elif self.direction == "DOWN":
            next_index = min(index +1, len(items) -1)
            
        items.move(index, next_index)
        export_data.items_index = next_index
        
        return{'FINISHED'}


classes = (
    Paladin_OT_ExportItemAdd, 
    Paladin_OT_ExportItemMove, 
    Paladin_OT_ExportItemRemove
    )
    
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
