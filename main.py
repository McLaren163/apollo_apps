from src.config import shiftgate_view_config
from src.config import TYPE_MAP_FILE
from src.models import ShiftGateModel, DesignModelMap
from src.views import ShiftGateView
from src.controllers import Controller
from src.validators import Validator


def main():
    model = ShiftGateModel(Validator(), DesignModelMap(TYPE_MAP_FILE))
    view = ShiftGateView(shiftgate_view_config)
    controller = Controller(view, model)
    view.mainloop()


if __name__ == "__main__":
    main()
