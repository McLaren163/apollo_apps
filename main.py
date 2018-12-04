CONFIG_FILE = 'view_config.json'


def main():
    import json
    from src.model import Model
    from src.view import View
    from src.controler import Controler

    conf = None
    with open(CONFIG_FILE, 'r', encoding='utf8') as file:
        conf = json.load(file)

    model = Model()
    view = View(conf)
    Controler(view, model)
    view.mainloop()
    print('after mainloop')


if __name__ == "__main__":
    main()
