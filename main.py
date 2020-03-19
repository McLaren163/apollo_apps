import os

CWD = os.path.abspath(os.path.dirname(__file__))
os.chdir(CWD)
print('Change CWD to:', CWD)

from src import config as CFG
from src.models import ShiftGateModel, DesignModelMap
from src.views import ShiftGateView
from src.controllers import Controller


debugState = {'order': 'Order',
              'customer': 'Customer',
              'date': 'Date',
              'engineer': 'Engineer',
              'model': 'Престиж',
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
              'console_column': 'П-образный 100х50',
              'console_column_height': '2200',
              'console_column_num': '2',
              'side': 'Вправо'}


def main():
    model = ShiftGateModel(DesignModelMap(CFG.FILES.get('gate_map')))
    view = ShiftGateView()
    controller = Controller(view, model)
    controller.start(start_state=debugState)


if __name__ == "__main__":
    main()
