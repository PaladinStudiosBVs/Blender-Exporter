# Addon info
bl_info = {
    "name": "Paladin Exporter",
    "description": "Export multiple assets",
    "author": "Joep Peeters, Laurens 't Jong",
    "blender": (3, 4, 0),
    "version": (0, 1, 4),
    "category": "3D View",
    "location": "View3D",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
}

if "bpy" in locals():
    # When developing, 'Reload Scripts' can be used in Blender to reload the add-on during runtime
    # This will ensure everything is reloaded if already loaded once before.
    import imp
    imp.reload(op_export_fbx)
    imp.reload(op_export_sets)
    imp.reload(panels)
    imp.reload(lists)
    imp.reload(properties)
    imp.reload(icons)
    imp.reload(general)
    print("Reloading")

import bpy
from .operators import op_export_fbx, op_export_sets
from .utilities import icons, general
from .ui import panels, lists
from .data import properties


modules = (op_export_fbx, op_export_sets, panels, lists, properties, icons)

def register():
    for module in modules:
        module.register()

    bpy.types.Scene.exporter = bpy.props.PointerProperty(type=data.properties.ExporterSceneProperties)

def unregister():
    del bpy.types.Scene.exporter

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
