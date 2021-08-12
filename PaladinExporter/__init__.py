# Addon info
bl_info = {
    "name": "Paladin Exporter",
    "description": "Export to Unity",
    "author": "Paladin Studios",
    "blender": (2, 93, 1),
    "version": (0, 0, 6),
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
    imp.reload(op_export_items_add)
    imp.reload(op_export_items_remove)
    imp.reload(view3d_pt_paladin_exporter)
    imp.reload(view3d_ul_export_list)
    imp.reload(export_data)
    imp.reload(export_item)
    print("Reloading")

import bpy
from PaladinExporter.Operators import op_export_fbx
from PaladinExporter.Operators import op_export_items_add
from PaladinExporter.Operators import op_export_items_remove
from PaladinExporter.Panels import view3d_pt_paladin_exporter
from PaladinExporter.Panels import view3d_ul_export_list
from PaladinExporter.Data import export_data
from PaladinExporter.Data import export_item

modules = (op_export_fbx, op_export_items_add, op_export_items_remove, view3d_pt_paladin_exporter, view3d_ul_export_list, export_data, export_item,)

def register():
    for module in modules:
        module.register()

    bpy.types.Scene.ExportData = bpy.props.PointerProperty(type=Data.export_data.ExportData)
    bpy.types.Scene.ExportItemsList = bpy.props.CollectionProperty(type = export_item.ExportItem) 
    bpy.types.Scene.ExportItemsIndex = bpy.props.IntProperty(name = "ExportItemsIndex", default = 0)
    
def unregister():
    del bpy.types.Scene.ExportData 
    del bpy.types.Scene.ExportItemsList
    del bpy.types.Scene.ExportItemsIndex

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
