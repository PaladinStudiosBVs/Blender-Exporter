# IMPORT

import os
from bpy.utils import previews

# ICON GETTER

icons = None

def get_icon(name):
    return icons[name].icon_id

# ICONS

def add_icons():
    global icons
    path = os.path.join(os.path.dirname(__file__), "icon_files")
    icons = previews.new()

    for i in sorted(os.listdir(path)):
        if not i.endswith(".png"):
            continue
        iconname = i[:-4]
        filepath = os.path.join(path, i)

        icons.load(iconname, filepath, 'IMAGE')

def remove_icons():
    global icons
    previews.remove(icons)

# REGISTER/UNREGISTER

def register():
    add_icons()

def unregister():
    remove_icons()
    