import bpy
from bpy.props import EnumProperty, IntProperty

class Paladin_OT_ExportSetAdd(bpy.types.Operator):
    bl_idname = "paladin.export_set_add"
    bl_label = "Add Set"
    bl_description = "Adds an export set"
    bl_options = {'UNDO'}
    
    def execute(self, context):
        context.scene.exporter.sets.add()
        return{'FINISHED'}

class Paladin_OT_ExportSetRemove(bpy.types.Operator):
    bl_idname = "paladin.export_set_remove"
    bl_label = "Remove Set"
    bl_description = "Delete this 'Export Set'"
    bl_options = {'UNDO'}

    index:IntProperty(name="set_index", default=0)

    @classmethod
    def poll(cls, context):
        export_data = context.scene.exporter
        return export_data.sets

    def execute(self, context):
        context.scene.exporter.sets.remove(self.index)
        return{'FINISHED'}

class Paladin_OT_ExportSetItemAdd(bpy.types.Operator):
    bl_idname = "paladin.export_set_items_add"
    bl_label = "Add"
    bl_options = {'UNDO'}

    set_index:IntProperty(name="Set Index", default=0)
    
    @classmethod
    def poll(cls, context):
        collection = context.collection
        if collection.name == 'Scene Collection':
            return False
        return True
            
    @classmethod
    def description(cls, context, event):
        collection = context.collection
        if collection.name == 'Scene Collection':
            return "You cannot add 'Scene Collection'"
        return f"Adds Collection '{collection.name}' to this export set"

    def execute(self, context):
        collection = context.collection
        export_set = context.scene.exporter.sets[self.set_index]
        
        for item in export_set.items:
            if item.name == collection.name:
                self.report({'WARNING'}, f"Collection '{collection.name}' already in set {self.set_index + 1}.")
                return {'CANCELLED'}
        
        item = export_set.items.add()
        item.name = collection.name
        export_set.items_index = len(export_set.items)-1
        return{'FINISHED'}

class Paladin_OT_ExportSetItemRemove(bpy.types.Operator):
    bl_idname = "paladin.export_set_item_remove"
    bl_label = "Remove set item"
    bl_options = {'UNDO'}
    bl_description = "Removes selected Item from this set"

    set_index:IntProperty(name="Set Index", default=0)

    def execute(self, context):
        export_set = context.scene.exporter.sets[self.set_index]
        items = export_set.items

        items.remove(export_set.items_index)
        # Selects item above index when it is removed:
        export_set.items_index = min(max(0, export_set.items_index - 1), len(items) - 1)
        return{'FINISHED'}

class Paladin_OT_ExportSetItemMove(bpy.types.Operator):
    bl_idname = "paladin.export_set_item_move"
    bl_label = "Move"
    bl_options = {'UNDO'}

    set_index:IntProperty(name="Set Index", default=0)
    direction: EnumProperty(items=[('UP', 'Up',""),('DOWN', 'Down',"")])

    @classmethod
    def description(cls, context, event):        
        return "Move Export Set Collection up or down"
    
    def execute(self, context):
        export_set = context.scene.exporter.sets[self.set_index]
        items = export_set.items
        index = export_set.items_index

        if self.direction == "UP":
            next_index = max(index -1, 0)
        elif self.direction == "DOWN":
            next_index = min(index +1, len(items) -1)
            
        items.move(index, next_index)
        export_set.items_index = next_index
        return{'FINISHED'}

classes = (
    Paladin_OT_ExportSetAdd,
    Paladin_OT_ExportSetRemove,
    Paladin_OT_ExportSetItemAdd, 
    Paladin_OT_ExportSetItemRemove,
    Paladin_OT_ExportSetItemMove,
    )
    
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
