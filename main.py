from src.config import shiftgate_view_config
from src.config import TYPE_MAP_FILE
from src.models import ShiftGateModel, DesignModelMap
from src.views import ShiftGateView
from src.controllers import Controller


debugState = {'order': 'Order',
              'customer': 'Customer',
              'date': 'Date',
              'engineer': 'Engineer',
              'width': '4000',
              'height': '2000',
              'cliarance': '100',
              'console': 'Треугольная',
              'side': 'Вправо'}


def main():
    model = ShiftGateModel(DesignModelMap(TYPE_MAP_FILE))
    view = ShiftGateView(shiftgate_view_config)
    controller = Controller(view, model)
    controller.start(start_state=debugState)


if __name__ == "__main__":
    main()
