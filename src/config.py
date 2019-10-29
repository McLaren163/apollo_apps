import json
import os

path = os.path.abspath(os.path.dirname(__file__))

CFG_VIEW_FILE = os.path.join('src', 'cfg', 'shiftgate_view_config.json')
CFG_MODEL_FILE = os.path.join('src', 'cfg', 'model_config.json')
TYPE_MAP_FILE = os.path.join('src', 'cfg', 'shiftgate_type_map.csv')
IMAGE_FOLDER = os.path.join('res', 'img')


shiftgate_view_config = None
with open(CFG_VIEW_FILE, 'r', encoding='utf8') as file:
    shiftgate_view_config = json.load(file)
