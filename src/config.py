import json

CFG_VIEW_FILE = '.\\src\\cfg\\view_config.json'
CFG_MODEL_FILE = '.\\src\\cfg\\model_config.json'
TYPE_MAP_FILE = '.\\src\\cfg\\type_map.csv'

view_config = None
with open(CFG_VIEW_FILE, 'r', encoding='utf8') as file:
    view_config = json.load(file)
