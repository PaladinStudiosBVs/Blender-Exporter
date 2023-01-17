import bpy
from bpy.props import BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty
from bpy.utils import register_classes_factory
from bpy.types import PropertyGroup


class ItemCollectionProperties(PropertyGroup):
    reset_origin: BoolProperty(name="Reset Origin", description="Enable, to place the object at the world origin when exporting.", default=True)
    include_in_export: BoolProperty(name="", description="Enable, to include when exporting", default=True)
    use_custom_path: BoolProperty(name="Custom Path", description="Enable, to use a custom export path", default=False)
    use_object_origin: BoolProperty(name="Relative Position", description="Enable, to have objects retain their relative position.", default=False)
    custom_path: StringProperty(name="Path", subtype='DIR_PATH', description="Custom export path for this collection.")
    collection_name: StringProperty()

class ExporterSceneProperties(PropertyGroup):
    
    items_list : CollectionProperty(type = ItemCollectionProperties)
    items_index: IntProperty(name = "ExportItemsIndex", default = 0)

    path: StringProperty(name='Path', subtype='DIR_PATH')
    active_collection_only: BoolProperty(name='Active collection only')
    include_meshes: BoolProperty(name='Include Meshes', default=True)
    bake_animation: BoolProperty(name='Bake Animation', default=False,)
    bake_anim_step: FloatProperty(name="Sampling Rate", default=1.0)
    bake_anim_simplify_factor: FloatProperty(name="Simplify", default=0.05)
    filename_suffix: StringProperty(name="Filename Suffix", default="_Animation")

classes = (ItemCollectionProperties, ExporterSceneProperties, )

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()

