import bpy
from bpy.props import StringProperty, IntProperty

class Paladin_OT_BrowsePath(bpy.types.Operator):
    bl_idname = "paladin.browse_path"
    bl_label = "Browse Path"
    bl_description = "Open a file browser to select the export directory"

    directory: StringProperty(subtype='DIR_PATH')
    set_index: IntProperty(default=-1)
    item_index: IntProperty(default=-1)

    def invoke(self, context, event):
        exporter = context.scene.exporter
        if self.item_index >= 0:
            current = exporter.sets[self.set_index].items[self.item_index].path
        else:
            current = exporter.sets[self.set_index].path

        if current and current != '//':
            self.directory = bpy.path.abspath(current)
        else:
            self.directory = bpy.path.abspath('//')

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        path = self.directory
        if bpy.data.is_saved:
            try:
                path = bpy.path.relpath(path)
            except ValueError:
                pass

        exporter = context.scene.exporter
        if self.item_index >= 0:
            exporter.sets[self.set_index].items[self.item_index].path = path
        else:
            exporter.sets[self.set_index].path = path

        return {'FINISHED'}

classes = (Paladin_OT_BrowsePath,)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
