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
    use_custom_path: bpy.props.BoolProperty(
        name="Custom Path",
        description="When false, the regular export path is used.",
    )
    custom_path: bpy.props.StringProperty(
        name="Path",
        subtype='DIR_PATH',
        description="Custom export path for this collection.",
    )

classes = (ExportItem,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
