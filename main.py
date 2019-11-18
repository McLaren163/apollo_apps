from src.config import shiftgate_view_config as view_config
from src.config import TYPE_MAP_FILE
from src.models import ShiftGateModel, DesignModelMap
from src.views import ShiftGateView
from src.controllers import Controller


debugState = {'order': 'Order',
              'customer': 'Customer',
              'date': 'Date',
              'engineer': 'Engineer',
              'width': '4000',
              'full_width': '6000',
              'height': '2000',
              'cliarance': '100',
              'console': 'Треугольная',
              'frame': '60х40x2',
              'filling': 'профлист СС10 шагрень 1ст',
              'kit': 'SG01',
              'frame_color': '8017',
              'filling_color': '9003',
              'color_type': 'Шагрень',
              'filling_weight': '10',
              'reception_column': 'Стандартный',
              'reception_column_height': '2100',
              'reception_column_num': '1',
              'beam': 'Продольная закладная',
              'rack': '4',
              'console_column': 'П-образный 60х40',
              'console_column_height': '2200',
              'console_column_num': '2',
              'side': 'Вправо'}


def main():
    model = ShiftGateModel(DesignModelMap(TYPE_MAP_FILE))
    view = ShiftGateView(view_config)
    controller = Controller(view, model)
    controller.start(start_state=debugState)


if __name__ == "__main__":
    main()
