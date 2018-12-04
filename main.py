CFG_VIEW_FILE = '.\\src\\cfg\\view_config.json'
CFG_MODEL_FILE = '.\\src\\cfg\\model_config.json'
TYPE_MAP_FILE = '.\\src\\cfg\\type_map.csv'


def main():
    import json
    from src.model import Model, ModelMap
    from src.view import View
    from src.controler import Controler

    conf = None
    with open(CFG_VIEW_FILE, 'r', encoding='utf8') as file:
        conf = json.load(file)

    model = Model(ModelMap(TYPE_MAP_FILE))
    view = View(conf)
    Controler(view, model)
    view.mainloop()


if __name__ == "__main__":
    main()
