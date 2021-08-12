import bpy

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

classes = (ExportData,)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
