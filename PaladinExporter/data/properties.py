from bpy.props import BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty
from bpy.utils import register_classes_factory
from bpy.types import PropertyGroup
from ..utilities.general import preset_items_get

class ExportItemProperties(PropertyGroup):
    include: BoolProperty(name="", description="Enable, to include when exporting", default=True)
    use_path: BoolProperty(name="Custom Path", description="Use a custom path, Click 'X' to disable", default=False)
    use_origin: BoolProperty(name="Relative Position", description="Enable, to have objects retain their relative position", default=False)
    use_collection: BoolProperty(name="Collection is Object", description="Enable, so the collection is the exported object", default=False)
    path: StringProperty(name="Path", subtype='DIR_PATH', description="Custom export path for this collection")
    name: StringProperty()

class ExportSetProperties(PropertyGroup):
    set_presets_get = preset_items_get()

    preset: EnumProperty(name='Set Preset', items=set_presets_get)
    path: StringProperty(name="Export Set Path", subtype='DIR_PATH', description="Export path for this Export Set")
    include: BoolProperty(name="Include Set", description="Enable, to include when exporting", default=True)
    prefix: StringProperty(name="Prefix", default="")
    suffix: StringProperty(name="Suffix", default="")
    items: CollectionProperty(type=ExportItemProperties)
    items_index: IntProperty(name="SetItemsIndex", default=0)

class ExporterSceneProperties(PropertyGroup):

    sets: CollectionProperty(type=ExportSetProperties)
    sets_index: IntProperty(name="ExportSetIndex", default=0)

classes = (ExportItemProperties, ExportSetProperties, ExporterSceneProperties, )

register, unregister = register_classes_factory(classes)

if __name__ == "__main__":
    register()

