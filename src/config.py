import json

CFG_VIEW_FILE = '.\\src\\cfg\\shiftgate_view_config.json'
CFG_MODEL_FILE = '.\\src\\cfg\\model_config.json'
TYPE_MAP_FILE = '.\\src\\cfg\\type_map.csv'

shiftgate_view_config = None
with open(CFG_VIEW_FILE, 'r', encoding='utf8') as file:
    shiftgate_view_config = json.load(file)
