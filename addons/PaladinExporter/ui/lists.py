import bpy
from ..utilities.icons import get_icon
from ..utilities.general import is_collection_valid
from ..utilities.general import get_collection_name

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        
        if not is_collection_valid(item.uuid):
            row.enabled = False
            row.label(text=f"Missing Collection!", icon='ERROR')
            return

        include = item.include
        path_false = get_icon('path_false')
        path_trueish = get_icon('path_expanded')
        path_true = get_icon('path_true')
        icon_collection = get_icon('collection_true') if item.use_collection else get_icon('collection_false')
        icon_origin = 'LOCKED' if item.use_origin else 'UNLOCKED'
        icon_include = 'CHECKBOX_HLT' if item.include else 'CHECKBOX_DEHLT'

        row.prop(item, 'include', icon_only=True, icon=icon_include, emboss=False)
        
        if item.use_path:
            split = row.split(factor=0.35)
            col_cell = split.column()
            col_cell.enabled = include
            col_cell.label(text=get_collection_name(item.uuid))
            path_cell = split.column()
            path_cell.prop(item, 'path', text="")
        else:
            col_cell = row.column()
            col_cell.enabled = include
            col_cell.label(text=get_collection_name(item.uuid))
        
        if item.use_path:
            row.prop(item, "use_path", icon_only=True, icon='RIGHTARROW', emboss=False)
        elif item.path:
            row.prop(item, "use_path", icon_only=True, icon_value=path_true, emboss=False)
        else:
            row.prop(item, "use_path", icon_only=True, icon_value=path_false, emboss=False)

        row.prop(item, 'use_origin', icon_only=True, icon=icon_origin, emboss=False)
        row.prop(item, 'use_collection', icon_only=True, icon_value=icon_collection, emboss=False)
        
classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
