import bpy

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):
        
        export_data = context.scene.exporter
        include = item.include_in_export

        if index >= 0 and export_data.items_list:
            
            item = export_data.items_list[index]

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

            

            row = layout.row(align=True)
            row.enabled = include

            col_cell = row.split(factor=0.5)
            
            col_cell.label(text=item.collection_name)

            path_cell = col_cell.split()
            
            path_cell.prop(item, 'custom_path', text="")

            row.prop(item, 'reset_origin', icon_only=True, icon='ORIENTATION_GLOBAL')

            row = layout.row(align=True)
            row.prop(item, 'include_in_export')
            

classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
