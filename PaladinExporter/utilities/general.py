import bpy, json, os, sys

def get_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def preset_path_get():
        path = get_path()
        return os.path.join(path, "presets")

def preset_items_get():
        preset_path = preset_path_get()
        preset_files = [file for file in os.listdir(preset_path) if file.endswith(".json")]
        items = [(
            os.path.basename(file), 
            json.load(open(os.path.join(preset_path, file)))["name"], 
            json.load(open(os.path.join(preset_path, file)))["description"]) for file in preset_files]
        return items

def is_collection_valid(collection_name):
    collections = bpy.data.collections
    for collection in collections:
        if collection.name == collection_name:
            return True
    return False

def has_export_sets():
    export_data = bpy.context.scene.exporter
    export_sets = export_data.sets
    
    if len(export_sets) < 1:
        return False
    return True

def has_sets_include():
    export_data = bpy.context.scene.exporter
    export_sets = export_data.sets

    for export_set in export_sets:
        has_include = False
        if export_set.include:
            has_include = True
            break
    return has_include

def included_sets_has_item():
    export_data = bpy.context.scene.exporter
    export_sets = export_data.sets

    for export_set in export_sets:
        has_items = False
        if export_set.include:
            if len(export_set.items) > 0:
                has_items = True
                break
    return has_items

def get_event_modifiers(event):
    ctrl = event.ctrl
    if sys.platform.startswith('darwin'):
        ctrl = event.oskey
    alt = event.alt
    shift = event.shift
    return ctrl, alt, shift

def get_export_path(export_set, export_item, filename):
    export_path = os.path.join(os.path.dirname(bpy.data.filepath), filename)
    if export_item.use_path and not export_item.path == "":
        export_path = os.path.join(export_item.path, filename)
    elif not export_set.path == "":
        export_path = os.path.join(export_set.path, filename)
    return export_path

object_types = ('MESH','EMPTY','ARMATURE')

def exportable(obj):
    return obj.parent == None and obj.type in object_types and obj.visible_get()

def exportable_selected(obj):
    return obj.parent == None and obj.type in object_types and obj.select_get() and obj.visible_get()

def exportable_selected_nested(obj):
    return obj.parent and obj.type in object_types and obj.select_get() and obj.parent.visible_get()
    
    

