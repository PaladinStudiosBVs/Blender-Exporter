import json, os

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

