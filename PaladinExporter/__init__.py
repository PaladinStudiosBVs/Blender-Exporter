# Addon info
bl_info = {
    "name": "Paladin Exporter",
    "description": "Export to Unity",
    "author": "Paladin Studios",
    "blender": (2, 93, 1),
    "version": (0, 1, 2),
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
    imp.reload(op_export_items)
    imp.reload(panels)
    imp.reload(lists)
    imp.reload(properties)
    print("Reloading")

import bpy
from .operators import op_export_fbx
from .operators import op_export_items
from .ui import panels
from .ui import lists
from .data import properties

modules = (op_export_fbx, op_export_items, panels, lists, properties)

def register():
    for module in modules:
        module.register()

    bpy.types.Scene.ExportData = bpy.props.PointerProperty(type=data.properties.ExportData)
    bpy.types.Scene.ExportItemsList = bpy.props.CollectionProperty(type = properties.ExportItem)
    bpy.types.Scene.ExportItemsIndex = bpy.props.IntProperty(name = "ExportItemsIndex", default = 0)
    
def unregister():
    del bpy.types.Scene.ExportData
    del bpy.types.Scene.ExportItemsList
    del bpy.types.Scene.ExportItemsIndex

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
