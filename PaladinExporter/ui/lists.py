import bpy
from ..utilities.icons import get_icon

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        collections = bpy.data.collections
        include = item.include_in_export
        icon_path = get_icon('custom_path')
        
        row = layout.row(align=True)

        collection_found = False
        for collection in collections:
            if collection.name == item.collection_name:
                collection_found = True
                break
        
        if not collection_found:
            row.enabled = False
            row.label(text=f"Missing Collection: '{item.collection_name}'", icon='ERROR')
            return

        row.prop(item, 'include_in_export')
      
        if item.use_custom_path:
            split = row.split(factor=0.35)
            col_cell = split.column()
            col_cell.enabled = include
            col_cell.label(text=item.collection_name)
            path_cell = split.column()
            path_cell.prop(item, 'custom_path', text="")
        else:
            col_cell = row.column()
            col_cell.enabled = include
            col_cell.label(text=item.collection_name)

        if item.use_custom_path:
            row.prop(item, 'use_custom_path', icon_only=True, icon='PANEL_CLOSE', emboss=False)
            col = row.column()
            col.prop(item, 'use_object_origin', icon_only=True, icon='OBJECT_ORIGIN')
        else: 
            row.prop(item, 'use_custom_path', icon_only=True, icon_value=icon_path)
            row.prop(item, 'use_object_origin', icon_only=True, icon='OBJECT_ORIGIN')
            
classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
