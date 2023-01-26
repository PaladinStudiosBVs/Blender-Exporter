import bpy
from ..utilities.icons import get_icon
from ..utilities.general import is_collection_valid

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        include = item.include
        icon_path = get_icon('custom_path')
        
        row = layout.row(align=True)

        if not is_collection_valid(item.name):
            row.enabled = False
            row.label(text=f"Missing Collection: '{item.name}'", icon='ERROR')
            return

        row.prop(item, 'include')
      
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
            row.prop(item, 'use_origin', icon_only=True, icon='OBJECT_ORIGIN', emboss=True)
            row.prop(item, 'use_collection', icon_only=True, icon='OUTLINER_COLLECTION', emboss=True)
        else: 
            row.prop(item, 'use_path', icon_only=True, icon_value=icon_path, emboss=True)
            row.prop(item, 'use_origin', icon_only=True, icon='OBJECT_ORIGIN', emboss=True)
            row.prop(item, 'use_collection', icon_only=True, icon='OUTLINER_COLLECTION', emboss=True)
            
classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
