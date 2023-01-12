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

class ExportData(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(
        name='Path',
        subtype='DIR_PATH',
    )
    active_collection_only: bpy.props.BoolProperty(
        name='Active collection only',
    )
    include_meshes: bpy.props.BoolProperty(
        name='Include Meshes',
        default=True,
    )
    bake_animation: bpy.props.BoolProperty(
        name='Bake Animation',
        default=False,
    )
    bake_anim_step: bpy.props.FloatProperty(
        name="Sampling Rate",
        default=1.0,
    )
    bake_anim_simplify_factor: bpy.props.FloatProperty(
        name="Simplify",
        default=0.05,
    )
    filename_suffix: bpy.props.StringProperty(
        name="Filename Suffix",
        default="_Animation",
    )

classes = (ExportItem, ExportData )

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
