import bpy, os, json

from ..operators import op_export_fbx, op_export_sets
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
        sets = export_data.sets

        export_icon = get_icon('icon_export')

        layout = self.layout
        layout.use_property_decorate = False

        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator(op_export_fbx.Paladin_OT_ExportFbx.bl_idname, text='', icon_value=export_icon)
        


        for i, set in enumerate(sets):
            layout = self.layout.box()
            self.draw_set(layout, set, i, export_data)

        layout = self.layout
        box = layout.box()
        box.operator(op_export_sets.Paladin_OT_ExportSetAdd .bl_idname, icon='ADD', text="", emboss=False)

    def draw_set(self, layout, set, index, export_data):
        items = set.items
        layout.use_property_decorate = False

        col = layout.column(align=True)
        row = col.row(align=False)
        
        row.prop(set, "set_include", text="")
        row.prop(set,'set_preset', text="", emboss=False)
        row.operator(op_export_sets.Paladin_OT_ExportSetRemove.bl_idname, icon='TRASH', text="", emboss=False).index=index

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
        row.template_list("VIEW3D_UL_ExportList", "items", set, "items", set, "items_index", rows=rows)
        
        col = row.column(align=True)

        col.operator(op_export_sets.Paladin_OT_ExportSetItemAdd .bl_idname, icon='ADD', text="").set_index=index
        
        row = col.row(align=True)
        if len(items) < 1:
            row.enabled = False
        row.operator(op_export_sets.Paladin_OT_ExportSetItemRemove .bl_idname, icon='REMOVE', text="").set_index=index
        #col.separator()
        if len(items) > 1:
            op = col.operator(op_export_sets.Paladin_OT_ExportSetItemMove.bl_idname, text="", icon="TRIA_UP")
            op.direction = "UP"
            op.set_index = index
            op = col.operator(op_export_sets.Paladin_OT_ExportSetItemMove.bl_idname, text="", icon="TRIA_DOWN")
            op.direction = "DOWN"
            op.set_index = index
            
        
classes = (VIEW3D_PT_Paladin_Exporter,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
