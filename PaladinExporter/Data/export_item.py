import bpy

class ExportItem(bpy.types.PropertyGroup):
    collection_name: bpy.props.StringProperty()
    reset_origin: bpy.props.BoolProperty(
        name="Reset Origin",
        description="When set to True, this will place the object at the world origin when exporting.",
    )
    include_in_export: bpy.props.BoolProperty(
        name="",
        description="Include when exporting",
        default=True,
    )

classes = (ExportItem,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
