import bpy, os, json

from ..operators import op_export_fbx, op_export_items, op_export_sets
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
        items = export_data.items_list
        export_icon = get_icon('icon_export')

        layout = self.layout
        layout.use_property_decorate = False

        row = layout.row(align=True)
        row.scale_y = 1.25
        row.operator(op_export_fbx.Paladin_OT_ExportFbx.bl_idname, text='Export', icon_value=export_icon)
        
        for i in range(len(set_list)):
            self.draw_set(set_list, i, items, export_data)

        box = layout.box()
        box.operator(op_export_sets.Paladin_OT_ExportSetAdd.bl_idname, icon='ADD', text="", emboss=False)

        print(set_index)

    def draw_set(self, set_list, index, items, export_data):
        set_index = index
        set = set_list[index]
        
        layout = self.layout
        layout.use_property_decorate = False
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=False)
        
        row.prop(set, "set_include", text="")
        row.prop(set,'set_preset', text="", emboss=False)
        row.operator(op_export_sets.Paladin_OT_ExportSetRemove.bl_idname, icon='TRASH', text="", emboss=False)

        col = box.column(align=True)
        col.use_property_split = True

        row = col.row(align=True)
        row.prop(set, "set_path", text="Path")
        row = col.row(align=True)
        row.prop(set, "set_prefix", text="Affixes")
        row.prop(set, "set_suffix", text="")

        box.use_property_split = False
        rows = 1
        if len(items) >= 2:
            rows = 3

        row = box.row()
        row.use_property_split = False
        row.template_list("VIEW3D_UL_ExportList", "items_list", export_data, "items_list", export_data, "items_index", rows=rows)
        
        col = row.column(align=True)
        col.operator(op_export_items.Paladin_OT_ExportItemAdd.bl_idname, icon='ADD', text="")
        col.operator(op_export_items.Paladin_OT_ExportItemRemove.bl_idname, icon='REMOVE', text="")

        col.separator()

        if len(items) >= 2:
            col.operator(op_export_items.Paladin_OT_ExportItemMove.bl_idname, text="", icon="TRIA_UP").direction = "UP"
            col.operator(op_export_items.Paladin_OT_ExportItemMove.bl_idname, text="", icon="TRIA_DOWN").direction = "DOWN"
        
    
        

    




    
        
    
classes = (VIEW3D_PT_Paladin_Exporter,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
