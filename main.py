from src.config import view_config
from src.config import TYPE_MAP_FILE
from src.model import Model, ModelMap
from src.view import View
from src.controler import Controler


def main():
    model = Model(ModelMap(TYPE_MAP_FILE))
    view = View(view_config)
    controler = Controler(view, model)
    view.mainloop()


if __name__ == "__main__":
    main()
