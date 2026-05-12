# Addon info
bl_info = {
    "name": "Game Exporter",
    "description": "Export models & animations to game engines such as Unity & Unreal",
    "author": "Joep Peters, Laurens 't Jong, Jelmer Kok, Jorrit de Vries",
    "blender": (3, 4, 1),
    "version": (1, 2, 4),
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
    imp.reload(op_browse_path)
    imp.reload(panels)
    imp.reload(lists)
    imp.reload(properties)
    imp.reload(items)
    imp.reload(icons)
    imp.reload(general)
    print("Reloading")

import bpy
from .operators import op_export_fbx, op_export_sets, op_browse_path
from .utilities import icons, general
from .ui import panels, lists
from .data import properties, items

modules = (op_export_fbx, op_export_sets, op_browse_path, panels, lists, properties, icons)

@bpy.app.handlers.persistent
def auto_export_on_save(filepath):
    print(f"[Game Exporter] save_post fired, filepath={filepath}")
    auto_export = bpy.context.scene.exporter.auto_export
    print(f"[Game Exporter] auto_export={auto_export}")
    if auto_export:
        print("[Game Exporter] Triggering export...")
        bpy.ops.paladin.exportfbx('EXEC_DEFAULT', export_selected=False)
        print("[Game Exporter] Export complete")

def register():
    for module in modules:
        module.register()

    bpy.types.Scene.exporter = bpy.props.PointerProperty(type=properties.ExporterSceneProperties)
    bpy.app.handlers.save_post.append(auto_export_on_save)

def unregister():
    if auto_export_on_save in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(auto_export_on_save)
    del bpy.types.Scene.exporter

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
