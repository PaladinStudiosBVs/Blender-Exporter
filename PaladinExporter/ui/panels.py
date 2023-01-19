import bpy, os, json

from ..operators import op_export_fbx, op_export_items, op_export_sets, op_export_set_items
from bpy.props import EnumProperty
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
        set_list = export_data.set_list
        set_index = export_data.set_index
        
        export_icon = get_icon('icon_export')

        layout = self.layout
        layout.use_property_decorate = False

        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(op_export_fbx.Paladin_OT_ExportFbx.bl_idname, text='', icon_value=export_icon)
        
        for i in range(len(set_list)):
            layout = self.layout.box()
            set = set_list[i]
            self.draw_set(layout,set, i)

        box = layout.box()
        box.operator(op_export_sets.Paladin_OT_ExportSetAdd.bl_idname, icon='ADD', text="", emboss=False)

    def draw_set(self, layout, set, index):
        items = set.set_items_list
        
        layout.use_property_decorate = False
        
        col = layout.column(align=True)
        row = col.row(align=False)
        
        row.prop(set, "set_include", text="")
        row.prop(set,'set_preset', text="", emboss=False)
        row.operator(op_export_sets.Paladin_OT_ExportSetRemove.bl_idname, icon='TRASH', text="", emboss=False).index = index

        col = layout.column(align=True)
        col.use_property_split = True

        row = col.row(align=True)
        row.prop(set, "set_path", text="Path")
        row = col.row(align=True)
        row.prop(set, "set_prefix", text="Affixes")
        row.prop(set, "set_suffix", text="")

        layout.use_property_split = False
        rows = 2
        if len(items) >= 2:
            rows = 3

        row = layout.row()
        row.use_property_split = False
        row.template_list("VIEW3D_UL_ExportList", "set_items_list", set, "set_items_list", set, "set_items_index", rows=rows)
        
        col = row.column(align=True)
        col.operator(op_export_set_items.Paladin_OT_SetExportItemAdd.bl_idname, icon='ADD', text="")
        col.operator(op_export_set_items.Paladin_OT_SetExportItemRemove.bl_idname, icon='REMOVE', text="")

        col.separator()
        '''
        if len(items) >= 2:
            col.operator(op_export_items.Paladin_OT_ExportItemMove.bl_idname, text="", icon="TRIA_UP").direction = "UP"
            col.operator(op_export_items.Paladin_OT_ExportItemMove.bl_idname, text="", icon="TRIA_DOWN").direction = "DOWN"
            '''
        
    
        

    




    
        
    
classes = (VIEW3D_PT_Paladin_Exporter,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
