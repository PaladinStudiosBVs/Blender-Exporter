import bpy

from ..operators import op_export_fbx
from ..operators import op_export_items

class VIEW3D_PT_Paladin_Exporter(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Paladin_Exporter_Panel"
    bl_label = "Paladin Exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Paladin Studios"
    bl_order = 0

    def draw(self, context):
        export_data = context.scene.exporter
        items = export_data.items_list
        
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        
        row = layout.row(align=True)
        row.prop(export_data,'path', text='Global Path')

        layout.use_property_split = False
        row = layout.row()
        row.template_list("VIEW3D_UL_ExportList", "items_list", export_data, "items_list", export_data, "items_index")
        
        col = row.column(align=True)
        col.operator(op_export_items.Paladin_OT_ExportItemAdd.bl_idname, icon='ADD', text="")
        col.operator(op_export_items.Paladin_OT_ExportItemRemove.bl_idname, icon='REMOVE', text="")

        col.separator()

        if len(items) >= 2:
            col.operator(op_export_items.Paladin_OT_ExportItemMove.bl_idname, text="", icon="TRIA_UP").direction = "UP"
            col.operator(op_export_items.Paladin_OT_ExportItemMove.bl_idname, text="", icon="TRIA_DOWN").direction = "DOWN"

        row = layout.row()
        row.prop(export_data, 'include_meshes')
        row.prop(export_data, 'bake_animation')

        layout.use_property_split = True

        if export_data.bake_animation:
            row = layout.row()
            row.prop(export_data, 'bake_anim_step')
            row = layout.row()
            row.prop(export_data, 'bake_anim_simplify_factor')
            row = layout.row()
            row.prop(export_data, 'filename_suffix')
        
        row = layout.row()
        row.scale_y = 1.5
        row.operator(op_export_fbx.Paladin_OT_ExportFbx.bl_idname, text='Export', icon='EXPORT')
    
classes = (VIEW3D_PT_Paladin_Exporter,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
