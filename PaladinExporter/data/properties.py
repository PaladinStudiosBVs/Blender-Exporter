from bpy.props import BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty
from bpy.utils import register_classes_factory
from bpy.types import PropertyGroup
from ..utilities.general import preset_items_get

#preset_items = []

class ItemCollectionProperties(PropertyGroup):
    reset_origin: BoolProperty(name="Reset Origin", description="Enable, to place the object at the world origin when exporting", default=True)
    include_in_export: BoolProperty(name="", description="Enable, to include when exporting", default=True)
    use_custom_path: BoolProperty(name="Custom Path", description="Use a custom path, Click 'X' to disable", default=False)
    use_object_origin: BoolProperty(name="Relative Position", description="Enable, to have objects retain their relative position", default=False)
    custom_path: StringProperty(name="Path", subtype='DIR_PATH', description="Custom export path for this collection")
    collection_name: StringProperty()

class ExportSetCollectionProperties(PropertyGroup):

    set_presets_get = preset_items_get()

    set_preset: EnumProperty(name='Set Preset', items=set_presets_get)
    set_path: StringProperty(name="Export Set Path", subtype='DIR_PATH', description="Export path for this Export Set")
    set_include: BoolProperty(name="Include Set", description="Enable, to include when exporting", default=True)
    set_prefix: StringProperty(name="Prefix", default="")
    set_suffix: StringProperty(name="Suffix", default="")

    items: CollectionProperty(type=ItemCollectionProperties)
    items_index: IntProperty(name="SetItemsIndex", default=0)

class ExporterSceneProperties(PropertyGroup):

    sets: CollectionProperty(type=ExportSetCollectionProperties)
    sets_index: IntProperty(name="ExportSetIndex", default=0)


classes = (ItemCollectionProperties, ExportSetCollectionProperties, ExporterSceneProperties, )

register, unregister = register_classes_factory(classes)

if __name__ == "__main__":
    register()

