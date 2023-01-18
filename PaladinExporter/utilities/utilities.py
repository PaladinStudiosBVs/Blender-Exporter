import json, os

def preset_items_get(path):
        preset_files = [file for file in os.listdir(path) if file.endswith(".json")]
        items = [(
            json.load(open(os.path.join(path, file)))["item"], 
            json.load(open(os.path.join(path, file)))["name"], 
            json.load(open(os.path.join(path, file)))["description"]) for file in preset_files]
        return items

def scan_json_file(self, path):
    json_files = []
    
    for file_name in os.listdir(path):
        if file_name.endswith(".json"):
            json_files.append(f"{path}/{file_name}")
    return json_files
