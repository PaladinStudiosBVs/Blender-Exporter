import bpy
from ..utilities.icons import get_icon

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):
        
        export_data = context.scene.exporter
        include = item.include_in_export
        custom_path = get_icon('custom_path')

        #arrow_left = get_icon('arrow_left')
        
        if index >= 0 and export_data.items_list:
            
            item = export_data.items_list[index]

            #failsafe to keep export settings like they were
            #if item.reset_origin:
                #item.use_object_origin = False

            collection_found = False
            for collection in bpy.data.collections:
                if collection.name == item.collection_name:
                    collection_found = True
                    break

            row = layout.row(align=True)
            
            if not collection_found:
                row.enabled = False
                row.label(text=f"Missing: '{item.collection_name}'", icon='ERROR')
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
            else: 
                row.prop(item, 'use_custom_path', icon_only=True, icon_value=custom_path)  
            row.prop(item, 'use_object_origin', icon_only=True, icon='OBJECT_ORIGIN')

            

classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
