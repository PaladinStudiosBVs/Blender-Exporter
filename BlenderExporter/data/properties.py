import bpy
from bpy.props import BoolProperty, StringProperty, FloatProperty, IntProperty, CollectionProperty, EnumProperty
from bpy.utils import register_classes_factory
from bpy.types import PropertyGroup
from ..utilities.general import preset_items_get

def make_path_relative(self, context):
    if self.path and not self.path.startswith('//') and bpy.data.is_saved:
        try:
            self.path = bpy.path.relpath(self.path)
        except ValueError:
            pass

def update_export_preset(self, context):
    """Springt checkbox aan bij SPO, uit bij andere presets"""
    try:
        enum_items = self.bl_rna.properties["preset"].enum_items
        preset_name = enum_items[self.preset].name
        force_on = (preset_name == "Substance Painter Object")
        for export_item in self.items:
            export_item.use_collection = force_on
    except Exception as e:
        print("update_export_preset error:", e)

class ExportItemProperties(PropertyGroup):
    include: BoolProperty(name="", description="Enable, to include when exporting", default=True)
    use_path: BoolProperty(name="Show Path", description="Show or hide 'Export Item Path'", default=False)
    use_origin: BoolProperty(name="Lock Position", description="If locked, objects will not be moved to world '0.0.0'", default=False)
    use_collection: BoolProperty(name="Collection is Object", description="If enabled, the collection is the exported object", default=False)
    include_hidden: BoolProperty(name="Include Hidden", description="If enabled, hidden objects are also exported", default=False)
    path: StringProperty(name="Path", subtype='NONE', description="Custom export path for this collection", default='//', update=make_path_relative)
    name: StringProperty(description="")
    uuid: StringProperty(description="")

class ExportSetProperties(PropertyGroup):
    preset: EnumProperty(name='Set Preset', items=preset_items_get(), update=update_export_preset)
    has_path:BoolProperty(name="Show Path", description="Show or hide 'Export Set Path", default=True)
    path: StringProperty(name="Export Set Path", subtype='NONE', description="Export path for this Export Set", default='//', update=make_path_relative)
    include: BoolProperty(name="Include Set", description="Enable, to include when exporting", default=True)
    has_affixes:BoolProperty(name="Show Affixes", description="Show or hide export set 'Affixes'", default=False )
    prefix: StringProperty(name="Prefix", default="")
    suffix: StringProperty(name="Suffix", default="")
    items: CollectionProperty(type=ExportItemProperties)
    items_index: IntProperty(name="Collection", default=0)

class ExporterSceneProperties(PropertyGroup):
    sets: CollectionProperty(type=ExportSetProperties)
    auto_export: BoolProperty(
        name="Auto Export on Save",
        description="Automatically export when the .blend file is saved",
        default=False
    )

classes = (ExportItemProperties, ExportSetProperties, ExporterSceneProperties)

register, unregister = register_classes_factory(classes)

if __name__ == "__main__":
    register()
