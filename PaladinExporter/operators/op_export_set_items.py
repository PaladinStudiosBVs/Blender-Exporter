import bpy
from bpy.props import EnumProperty, IntProperty

class Paladin_OT_SetExportItemRemove(bpy.types.Operator):
    bl_idname = "paladin.export_set_item_remove"
    bl_label = "Remove set item"

    @classmethod
    def poll(cls, context):
        export_data = context.scene.exporter
        set_data = export_data.set_list[0]
        items = set_data.set_items_list
        return items

    @classmethod
    def description(cls, context, event):
        export_data = context.scene.exporter
        set_data = export_data.set_list[0]
        items = set_data.set_items_list

        if not items:
            return "No Export Collection to Remove"
        return "Remove selected Export Collection from export list"
    
    def execute(self, context):
        export_data = context.scene.exporter
        set_data = export_data.set_list[0]
        items = set_data.set_items_list
        index = set_data.set_items_index

        items.remove(index)
        # Selects item above index when it is removed:
        set_data.set_items_index = min(max(0, index - 1), len(items) - 1)
        return{'FINISHED'}


class Paladin_OT_SetExportItemAdd(bpy.types.Operator):
    bl_idname = "paladin.export_set_items_add"
    bl_label = "Add"

    @classmethod
    def poll(cls, context):
        collection = context.collection
        export_data = context.scene.exporter
        set_data = export_data.set_list[0]
        items = set_data.set_items_list

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
        set_data = export_data[0].set_list
        items = set_data.set_items_list

        if collection is None:
            return "There are no collections in the scene"
        for item in items:
            if item.collection_name == collection.name:
                return f"Collection '{collection.name}' is already in the export list"
        return f"Adds Collection '{collection.name}' to the export list"
    
    def execute(self, context):
        collection = context.collection
        export_data = context.scene.exporter
        set_data = export_data.set_list[0]
        items = set_data.set_items_list

        item = items.add()
        item.collection_name = collection.name
        
        set_data.set_item_index = len(items)-1
        return{'FINISHED'}

class Paladin_OT_SetExportItemMove(bpy.types.Operator):
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
    Paladin_OT_SetExportItemAdd, 
    Paladin_OT_SetExportItemMove, 
    Paladin_OT_SetExportItemRemove
    )
    
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
