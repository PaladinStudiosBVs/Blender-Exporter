import bpy
from ..utilities.icons import get_icon
from ..utilities.general import is_collection_valid

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        include = item.include
        icon_path = get_icon('custom_path')
        collection_false = get_icon('collection_false')
        collection_true = get_icon('collection_true')
        
        row = layout.row(align=True)

        if not is_collection_valid(item.name):
            row.enabled = False
            row.label(text=f"Missing Collection: '{item.name}'", icon='ERROR')
            return

        if include:
            row.prop(item, 'include', icon_only=True, icon='CHECKBOX_HLT', emboss=False)
        else:
            row.prop(item, 'include', icon_only=True, icon='CHECKBOX_DEHLT', emboss=False)

        if item.use_path:
            split = row.split(factor=0.35)
            col_cell = split.column()
            col_cell.enabled = include
            col_cell.label(text=item.name)
            path_cell = split.column()
            path_cell.prop(item, 'path', text="")
        else:
            col_cell = row.column()
            col_cell.enabled = include
            col_cell.label(text=item.name)

        if item.use_path:
            row.prop(item, 'use_path', icon_only=True, icon='PANEL_CLOSE', emboss=False)
        else:
            row.prop(item, 'use_path', icon_only=True, icon_value=icon_path, emboss=False)
        
        if item.use_origin:
            row.prop(item, 'use_origin', icon_only=True, icon='LOCKED', emboss=False)
        else:
            row.prop(item, 'use_origin', icon_only=True, icon='UNLOCKED', emboss=False)
        
        if item.use_collection:
            row.prop(item, 'use_collection', icon_only=True, icon_value=collection_true, emboss=False)
        else:
            row.prop(item, 'use_collection', icon_only=True, icon_value=collection_false, emboss=False)

        
            
classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
