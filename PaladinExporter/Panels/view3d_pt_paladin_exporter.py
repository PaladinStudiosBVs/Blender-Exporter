import bpy

from ..Operators import op_export_fbx
from ..Operators import op_export_items_add
from ..Operators import op_export_items_remove
from ..Data import export_data
from . import view3d_ul_export_list

class VIEW3D_PT_Paladin_Exporter(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Paladin_Exporter_Panel"
    bl_label = "Paladin Exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Paladin Studios"

    def draw(self, context):
        layout = self.layout
        

        row = layout.row()
        row.prop(context.scene.ExportData,'path')

        ##row = layout.row()
        ##row.prop(context.scene.ExportData,'selected_objects_only')

        row = layout.row()
        row.template_list("VIEW3D_UL_ExportList", "ExportItemsList", context.scene, "ExportItemsList", context.scene, "ExportItemsIndex")
        row.enabled = not context.scene.ExportData.selected_objects_only
        
        row = layout.row()
        row.operator(op_export_items_add.Paladin_OT_AddExportItem.bl_idname)
        row.operator(op_export_items_remove.Paladin_OT_RemoveExportItem.bl_idname)

        row = layout.row()
        row.prop(context.scene.ExportData, 'include_meshes')
        row.prop(context.scene.ExportData, 'bake_animation')

        layout.use_property_split = True

        if context.scene.ExportData.bake_animation:
            row = layout.row()
            row.prop(context.scene.ExportData, 'bake_anim_step')
            row = layout.row()
            row.prop(context.scene.ExportData, 'bake_anim_simplify_factor')
            row = layout.row()
            row.prop(context.scene.ExportData, 'filename_suffix')
        
        row = layout.row()
        row.operator(op_export_fbx.Paladin_OT_ExportFbx.bl_idname)
    
classes = (VIEW3D_PT_Paladin_Exporter,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
