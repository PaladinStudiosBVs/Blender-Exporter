import bpy

class VIEW3D_UL_ExportList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        scene = context.scene

        # Todo: decide proper icon
        custom_icon = 'OUTLINER_COLLECTION'

        # Todo: figure out what to do if we need to support all layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon = custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)

        if index >= 0 and scene.ExportItemsList:
            item = scene.ExportItemsList[index]

            row = layout.row()
            row.prop(item, 'include_in_export')

            row = layout.row()
            row.enabled = item.include_in_export

            collection_found = False
            for collection in bpy.data.collections:
                if collection.name == item.collection_name:
                    collection_found = True
                    break
            
            if not collection_found:
                row.label(text="Missing collection " + item.collection_name)
                return

            row.label(text=item.collection_name)
            row.prop(item, 'use_custom_path')
           
            split = row.split()
            split.enabled = item.use_custom_path
            split.prop(item, 'custom_path')

            row.prop(item, 'reset_origin')


classes = (VIEW3D_UL_ExportList,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
