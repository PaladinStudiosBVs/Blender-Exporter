import bpy
from ..utilities.icons import get_icon
from ..utilities.general import is_collection_valid

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        collections = bpy.data.collections
        include = item.item_include
        icon_path = get_icon('custom_path')
        
        row = layout.row(align=True)

        if not is_collection_valid(item.item_name):
            row.enabled = False
            row.label(text=f"Missing Collection: '{item.item_name}'", icon='ERROR')
            return

        row.prop(item, 'item_include')
      
        if item.item_use_path:
            split = row.split(factor=0.35)
            col_cell = split.column()
            col_cell.enabled = include
            col_cell.label(text=item.item_name)
            path_cell = split.column()
            path_cell.prop(item, 'item_path', text="")
        else:
            col_cell = row.column()
            col_cell.enabled = include
            col_cell.label(text=item.item_name)

        if item.item_use_path:
            row.prop(item, 'item_use_path', icon_only=True, icon='PANEL_CLOSE', emboss=False)
            col = row.column()
            col.prop(item, 'item_use_origin', icon_only=True, icon='OBJECT_ORIGIN')
        else: 
            row.prop(item, 'item_use_path', icon_only=True, icon_value=icon_path)
            row.prop(item, 'item_use_origin', icon_only=True, icon='OBJECT_ORIGIN')
            row.prop(item, 'item_use_collection', icon_only=True, icon='OUTLINER_COLLECTION')
            
classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
