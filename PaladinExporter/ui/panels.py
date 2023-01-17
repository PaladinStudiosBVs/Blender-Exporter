import bpy

from ..operators import op_export_fbx, op_export_items
from ..utilities.icons import get_icon

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
        export_icon = get_icon('icon_export')
        
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
        
        row = layout.row(align=True)
        row.scale_y = 1.25
        row.operator(op_export_fbx.Paladin_OT_ExportFbx.bl_idname, text='Export', icon_value=export_icon)
        
        #export_sel = split.column()
        #row.operator(op_export_fbx.Paladin_OT_ExportFbx.bl_idname, text='Selected', icon_value=export_icon)
    
        
    
classes = (VIEW3D_PT_Paladin_Exporter,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
