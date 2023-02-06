import bpy, json, os, sys

def get_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def preset_path_get():
    return os.path.join(get_path(), "presets")

def preset_items_get():
    return [(
        os.path.basename(file),
        json.load(open(os.path.join(preset_path_get(), file)))["name"],
        json.load(open(os.path.join(preset_path_get(), file)))["description"]) 
        for file in os.listdir(preset_path_get()) if file.endswith(".json")]

def is_collection_valid(item_name):
    return any(collection.name == item_name for collection in bpy.data.collections)

def has_sets_include(export_sets):
    return any(export_set.include for export_set in export_sets)

def included_sets_has_item(export_sets):
    return any(export_set.include and export_set.items for export_set in export_sets)
    
def get_event_modifiers(event):
    ctrl = event.ctrl
    if sys.platform.startswith('darwin'):
        ctrl = event.oskey
    alt = event.alt
    shift = event.shift
    return ctrl, alt, shift

def get_export_path(export_set, export_item, filename):
    return os.path.join(export_item.path or export_set.path or os.path.dirname(bpy.data.filepath), filename)

object_types = ('MESH','EMPTY','ARMATURE')

def exportable(obj):
    return obj.parent == None and obj.type in object_types and obj.visible_get()

def exportable_selected(obj):
    return obj.parent == None and obj.type in object_types and obj.select_get() and obj.visible_get()

def exportable_selected_nested(obj):
    return obj.parent and obj.type in object_types and obj.select_get() and obj.parent.visible_get()
    
    

