import bpy

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        scene = context.scene
        custom_icon = 'OUTLINER_COLLECTION'

        if index >= 0 and scene.ExportItemsList:
            item = scene.ExportItemsList[index]

            collection_found = False
            for collection in bpy.data.collections:
                if collection.name == item.collection_name:
                    collection_found = True
                    break

            if not collection_found:
                custom_icon = 'ERROR'

            # Todo: figure out what to do if we need to support all layout types
            if self.layout_type in {'DEFAULT', 'COMPACT'}:
                layout.label(text=item.name, icon = custom_icon)

            elif self.layout_type in {'GRID'}:
                layout.alignment = 'CENTER'
                layout.label(text="", icon = custom_icon)                    
            
            row = layout.row()

            if not collection_found:
                row.enabled = False
                row.label(text="Missing: " + item.collection_name)
                return

            row.prop(item, 'include_in_export')

            itemCell = row.split()

            itemCell.enabled = item.include_in_export

            itemCell.label(text=item.collection_name)
            itemCell.prop(item, 'use_custom_path')
           
            pathCell = itemCell.split()
            pathCell.enabled = item.use_custom_path
            pathCell.prop(item, 'custom_path')

            itemCell.prop(item, 'reset_origin')


classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
