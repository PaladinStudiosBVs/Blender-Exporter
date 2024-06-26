# Addon info
bl_info = {
    "name": "Game Exporter",
    "description": "Export models & animations to game engines such as Unity & Unreal",
    "author": "Joep Peters, Laurens 't Jong",
    "blender": (3, 4, 1),
    "version": (1, 2, 2),
    "category": "Import-Export",
    "location": "View3D > Sidebar > Game Exporter",
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
    imp.reload(items)
    imp.reload(icons)
    imp.reload(general)
    print("Reloading")

import bpy
from .operators import op_export_fbx, op_export_sets
from .utilities import icons, general
from .ui import panels, lists
from .data import properties, items

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
