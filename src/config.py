import os

PWD = os.path.abspath(os.path.dirname(__file__))

TYPE_MAP_FILE = os.path.join('src', 'cfg', 'shiftgate_type_map.csv')


def get_filepath(dir, filename):
    return os.path.join(FOLDERS.get(dir), filename)


FOLDERS = {
    'ico': os.path.join('res', 'icons'),
    'img': os.path.join('res', 'img'),
    'cfg': os.path.join('src', 'cfg')
}

FILES = {
    'icon': get_filepath('ico', 'logo.ico'),
    'gate_map': get_filepath('cfg', 'shiftgate_type_map.csv'),
}

GUI = {
    'title': 'Откатные ворота "АПОЛЛО"',
    'win_width': 600,
    'win_height': 600,
    'size_text': [18, 1],
    'size_input': [25, 1],
    'size_combo': [22, 1],
    'size_multiline': [45, 5],
    'fonts': {
        'normal': [
            'Calibri',
            '8'
        ],
        'bold': [
            'Calibri',
            '8',
            'bold'
        ]
    }
}

PDF = {
    'creator': 'fpdf'
}

GATE_IMAGES = {
    'drafts': {
        'ATL': 'atl.png',
        'APL': '',
        'ATR': 'atr.png',
        'APL': '',
        'BPL': '',
        'BPL': '',
        'CPL': '',
        'CPL': '',
        'DPL': '',
        'DPL': '',
        'EPL': '',
        'EPL': '',
        'FPL': '',
        'FPL': '',
    },
    'beams': {
        "Без опорной балки": 'xxx.png',
        "Опорная балка": 'xxx.png',
        "Продольная закладная": 'xxx.png',
        "Нестандарт": 'xxx.png'
    }
}

NO = 'НЕТ'

YES = 'ДА'

CONSOLE_TYPES = (
    'Треугольная',
    'Прямоугольная'
)

KIT_TYPES = {
    "SG01": {
        "max_weight": 500,
        "max_length": 5,
        "size": "70x60x3.5",
        "weight": 5.65
    },
    "МИКРО": {
        "max_weight": 350,
        "max_length": 4,
        "size": "60x55x3.0",
        "weight": 4.40
    },
    "ЭКО": {
        "max_weight": 500,
        "max_length": 5,
        "size": "70x60x3.5",
        "weight": 5.60
    },
    "ЕВРО": {
        "max_weight": 800,
        "max_length": 7,
        "size": "90x75x4.5",
        "weight": 9.20
    }
}

FRAME_TYPES = (
    '60х40x2',
    '80х40x2'
)

FILLING_TYPES = {
    "профлист СС10 шагрень 1ст": {
        "weight": 4.65
    },
    "профлист СС10 шагрень 2ст": {
        "weight": 9.30
    },
    "металлосайдинг с 2 сторон": {
        "weight": 12.00
    },
    "металлосайдинг декор": {
        "weight": 12.00
    }
}

COLOR_TYPES = (
    'Шагрень',
    'Матовый',
    'Глянец'
)

BEAM_TYPES = tuple(GATE_IMAGES['beams'])

COLUMN_TYPES = (
    'Стандартный',
    'П-образный 100х50'
)

SIDE_TYPES = (
    'Вправо',
    'Влево'
)

WIDGETS = {
    'order': {
        'text': '№ Заказа',
        'values': None
    },
    'engineer': {
        'text': 'Инженер',
        'values': None
    },
    'customer': {
        'text': 'Заказчик',
        'values': None
    },
    'date': {
        'text': 'Дата монтажа',
        'values': None
    },
    'width': {
        'text': 'Ширина проема, мм',
        'values': None
    },
    'full_width': {
        'text': 'Ширина полотна, мм',
        'values': None
    },
    'cliarance': {
        'text': 'Просвет, мм',
        'values': None
    },
    'height': {
        'text': 'Высота полотна, мм',
        'values': None
    },
    'side': {
        'text': 'Вид со двора',
        'values': SIDE_TYPES
    },
    'console': {
        'text': 'Консоль',
        'values': CONSOLE_TYPES
    },
    'kit': {
        'text': 'Комплектация',
        'values': tuple(KIT_TYPES)
    },
    'frame': {
        'text': 'Рама',
        'values': FRAME_TYPES
    },
    'frame_color': {
        'text': 'Цвет рамы',
        'values': None
    },
    'filling': {
        'text': 'Наполнение',
        'values': tuple(FILLING_TYPES)
    },
    'filling_weight': {
        'text': 'Вес м2 наполнения, кг',
        'values': None
    },
    'filling_color': {
        'text': 'Цвет наполнения',
        'values': None
    },
    'color_type': {
        'text': 'Тип покраски',
        'values': COLOR_TYPES
    },
    'beam': {
        'text': 'Опорная балка',
        'values': BEAM_TYPES
    },
    'rack': {
        'text': 'Зубчатая рейка, шт',
        'values': None
    },
    'reception_column': {
        'text': 'Приемный столб',
        'values': COLUMN_TYPES
    },
    'console_column': {
        'text': 'От бокового качения',
        'values': COLUMN_TYPES
    },
    'reception_column_height': {
        'text': 'Высота ПС, мм',
        'values': None
    },
    'console_column_height': {
        'text': 'Высота БК, мм',
        'values': None
    },
    'reception_column_num': {
        'text': 'Количество ПС, шт',
        'values': None
    },
    'console_column_num': {
        'text': 'Количество БК, шт',
        'values': None
    },
    'lock': {
        'text': 'Задвижка DH',
        'values': (
            NO,
            YES
        )
    },
    'door': {
        'text': 'Встроенная калитка',
        'values': '>Boolean<'
    },
    'decor': {
        'text': 'Переменный щит',
        'values': '>Boolean<'
    },
    'comments': {
        'values': '>Text<'
    }
}
