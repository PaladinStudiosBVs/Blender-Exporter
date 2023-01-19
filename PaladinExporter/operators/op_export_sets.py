import bpy
from bpy.props import IntProperty

class Paladin_OT_ExportSetAdd(bpy.types.Operator):
    bl_idname = "paladin.export_set_add"
    bl_label = "Add Set"
    bl_description = "Adds an export set"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        export_data = context.scene.exporter
        sets = export_data.set_list
        sets.add()
        return{'FINISHED'}

class Paladin_OT_ExportSetRemove(bpy.types.Operator):
    bl_idname = "paladin.export_set_remove"
    bl_label = "Remove Set"
    bl_description = "Removes an export set"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        export_data = context.scene.exporter
        return export_data.set_list

    def execute(self, context):
        export_data = context.scene.exporter
        sets = export_data.set_list
        index = export_data.set_index
        
        sets.remove(index)
        return{'FINISHED'}

classes = (
    Paladin_OT_ExportSetAdd, 
    Paladin_OT_ExportSetRemove
    )
    
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
