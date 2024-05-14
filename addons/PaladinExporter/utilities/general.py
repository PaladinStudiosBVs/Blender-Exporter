import bpy, json, os, sys, random
from ..data.items import export_object_types

UUID_PROPERTY = 'UUID'

def get_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def preset_path_get():
    return os.path.join(get_path(), "presets")

def preset_items_get():
    return [(
        os.path.basename(file),
        json.load(open(os.path.join(preset_path_get(), file)))["name"],
        json.load(open(os.path.join(preset_path_get(), file)))["description"]
        ) for file in os.listdir(preset_path_get()) if file.endswith(".json")]

# Returns if any collection exists with the a uuid property missing the provided uuid
def is_collection_valid(item_uuid):
    return any(collection.get(UUID_PROPERTY) == item_uuid for collection in bpy.data.collections)
    
# Returns the collection's name based on uuid
def get_collection_name(item_uuid):
    for collection in bpy.data.collections:
        if collection.get(UUID_PROPERTY) == item_uuid:
            return collection.name
    return None

def has_sets_include(export_sets):
    return any(export_set.include for export_set in export_sets)

def included_sets_has_item(export_sets):
    return any(export_set.include and export_set.items for export_set in export_sets)
    
def get_event_modifiers(event):
    ctrl = event.oskey if sys.platform.startswith('darwin') else event.ctrl
    alt = event.alt
    shift = event.shift
    return ctrl, alt, shift

def get_export_path(export_set, export_item, filename):
    return os.path.join(os.path.dirname(export_item.path) or os.path.dirname(export_set.path) or os.path.dirname(bpy.data.filepath), filename)

def exportable(obj):
    return obj.parent == None and obj.type in export_object_types and obj.visible_get()

def exportable_selected(obj):
    return obj.parent == None and obj.type in export_object_types and obj.select_get() and obj.visible_get()

def exportable_selected_nested(obj):
    return obj.parent and obj.type in export_object_types and obj.select_get() and obj.parent.visible_get()
    
def generate_random_uuid():
    uuid_bits = [random.randint(0, 255) for _ in range(16)]
    uuid_bits[6] = (uuid_bits[6] & 0x0f) | 0x40
    uuid_bits[8] = (uuid_bits[8] & 0x3f) | 0x80
    uuid_str = ''.join(['{:02x}'.format(byte) for byte in uuid_bits])
    return '-'.join([uuid_str[:8], uuid_str[8:12], uuid_str[12:16], uuid_str[16:20], uuid_str[20:]])