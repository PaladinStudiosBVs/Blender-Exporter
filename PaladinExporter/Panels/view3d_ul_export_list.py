import bpy

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        scene = context.scene

        if index >= 0 and scene.ExportItemsList:
            item = scene.ExportItemsList[index]

            collection_found = False
            for collection in bpy.data.collections:
                if collection.name == item.collection_name:
                    collection_found = True
                    break

            #layout.alignment = 'LEFT'
            row = layout.row(align=True)
            #row.scale_y = 1.2

            if not collection_found:
                row.enabled = False
                row.label(text=f"Missing: '{item.collection_name}'", icon='ERROR')
                return

            row.prop(item, 'include_in_export', icon_only=True, icon='EXPORT')
            row.prop(item, 'use_custom_path', icon_only=True, icon='FILEBROWSER')
            row.prop(item, 'reset_origin', icon_only=True, icon='ORIENTATION_GLOBAL')
            
            row.separator()

            coll_cell = row.split(factor=0.4)
            coll_cell.enabled = item.include_in_export
            coll_cell.label(text=item.collection_name)
            
            path_cell = coll_cell.split()
            path_cell.enabled = item.use_custom_path
            path_cell.prop(item, 'custom_path', text="")

classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
