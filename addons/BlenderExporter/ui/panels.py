import bpy

from ..operators import op_export_fbx, op_export_sets
from ..utilities.icons import get_icon

class VIEW3D_PT_Paladin_Exporter(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_Paladin_Exporter_Panel"
    bl_label = "Game Exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Paladin Studios"

    def draw(self, context):
        export_sets = context.scene.exporter.sets
        export_icon = get_icon('icon_export')
        icon_path_false = get_icon('path_false')
        icon_path_true = get_icon('path_true')
        icon_path_expanded = get_icon('path_expanded')
        icon_affix_false = get_icon('affix_false')
        icon_affix_true = get_icon('affix_true')
        icon_affix_expanded = get_icon('affix_expanded')
        export_selection_icon = get_icon('export_selection')
        remove_set = get_icon('remove_set')
        
        layout = self.layout
        layout.use_property_decorate = False

        row = layout.row(align=True)
        row.scale_y = 1.5
        col = row.row(align=True)
        
        col.operator(op_export_fbx.Paladin_OT_ExportFbx.bl_idname, text='Export', icon_value=export_icon).export_selected = False
        col.operator(op_export_fbx.Paladin_OT_ExportFbx.bl_idname, text='Selected', icon_value=export_selection_icon).export_selected = True

        for index, export_set in enumerate(export_sets):
            if export_set.has_path:
                icon_path = icon_path_expanded
            elif export_set.path:
                icon_path = icon_path_true
            else:
                icon_path = icon_path_false
            
            if export_set.has_affixes:
                icon_affix = icon_affix_expanded
            elif export_set.prefix or export_set.suffix:
                icon_affix = icon_affix_true
            else:
                icon_affix = icon_affix_false
            
            self.draw_set(export_set, index, remove_set, icon_path, icon_affix)

        box = self.layout.box()
        box.operator(op_export_sets.Paladin_OT_ExportSetAdd.bl_idname, icon='ADD', text="", emboss=False)

    def draw_set(self, export_set, index, remove_set, icon_path, icon_affix):
        items = export_set.items
        include = export_set.include
        layout = self.layout.box()
        layout.use_property_decorate = False

        row = layout.row(align=True)
        row.prop(export_set, "include", text="")
        split = row.split(factor=0.25, align=True)
        name_cell = split.column()
        name_cell. enabled = include
        name_cell.label(text=f"Set {index + 1}")
        preset_cell = split.column()
        preset_cell.prop(export_set,'preset', text="", emboss=True)
        
        row.prop(export_set, "has_path", icon_only=True, icon_value=icon_path, emboss=False) 
        row.prop(export_set, "has_affixes", icon_only=True, icon_value=icon_affix, emboss=False)
        
        row.operator(op_export_sets.Paladin_OT_ExportSetRemove.bl_idname, icon_value=remove_set, text="", emboss=False).index=index

        col = layout.column(align=True)
        col.use_property_split = True

        if export_set.has_path:
            row = col.row(align=True)
            row.prop(export_set, "path", text="Path")      
        if export_set.has_affixes:
            row = col.row(align=True)
            row.prop(export_set, "prefix", text="Affixes")
            row.prop(export_set, "suffix", text="")

        layout.use_property_split = False
        rows = 1
        if len(items) >= 2:
            rows = 3

        row = layout.row(align=True)
        row.use_property_split = False
        row.template_list("VIEW3D_UL_ExportList", f"Export Set {index}", export_set, "items", export_set, "items_index", rows=rows)
        
        col = row.column(align=True)
        col.operator(op_export_sets.Paladin_OT_ExportSetItemAdd.bl_idname, icon='ADD', text="", emboss=False).set_index=index
        
        row = col.row(align=True)
        if len(items) < 1:
            row.enabled = False
        row.operator(op_export_sets.Paladin_OT_ExportSetItemRemove.bl_idname, icon='REMOVE', text="", emboss=False).set_index=index
        if len(items) > 1:
            op = col.operator(op_export_sets.Paladin_OT_ExportSetItemMove.bl_idname, text="", icon="TRIA_UP", emboss=False)
            op.direction = "UP"
            op.set_index = index
            op = col.operator(op_export_sets.Paladin_OT_ExportSetItemMove.bl_idname, text="", icon="TRIA_DOWN", emboss=False)
            op.direction = "DOWN"
            op.set_index = index
                
classes = (VIEW3D_PT_Paladin_Exporter,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
