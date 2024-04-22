from bpy.props import BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty
from bpy.utils import register_classes_factory
from bpy.types import PropertyGroup
from ..utilities.general import preset_items_get

class ExportItemProperties(PropertyGroup):
    include: BoolProperty(name="", description="Enable, to include when exporting", default=True)
    use_path: BoolProperty(name="Show Path", description="Show or hide 'Export Item Path'", default=False)
    use_origin: BoolProperty(name="Lock Position", description="If locked, objects will not be moved to world '0.0.0'", default=False)
    use_collection: BoolProperty(name="Collection is Object", description="Enable, so the collection is the exported object", default=False)
    path: StringProperty(name="Path", subtype='DIR_PATH', description="Custom export path for this collection")
    name: StringProperty()
    uuid: StringProperty()

class ExportSetProperties(PropertyGroup):
    preset: EnumProperty(name='Set Preset', items=preset_items_get())
    has_path:BoolProperty(name="Show Path", description="Show or hide 'Export Set Path", default=True)
    path: StringProperty(name="Export Set Path", subtype='DIR_PATH', description="Export path for this Export Set")
    include: BoolProperty(name="Include Set", description="Enable, to include when exporting", default=True)
    has_affixes:BoolProperty(name="Show Affixes", description="Show or hide export set 'Affixes'", default=True )
    prefix: StringProperty(name="Prefix", default="")
    suffix: StringProperty(name="Suffix", default="")
    items: CollectionProperty(type=ExportItemProperties)
    items_index: IntProperty(name="SetItemsIndex", default=0)

class ExporterSceneProperties(PropertyGroup):

    sets: CollectionProperty(type=ExportSetProperties)

classes = (ExportItemProperties, ExportSetProperties, ExporterSceneProperties, )

register, unregister = register_classes_factory(classes)

if __name__ == "__main__":
    register()

