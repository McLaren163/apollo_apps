import os


HOMEDIR = os.path.expanduser('~')

CWD = os.getcwd()
print('CWD from config:', CWD)

FOLDERS = {
    'icons': os.path.join(CWD, 'res', 'icons'),
    'images': os.path.join(CWD, 'res', 'images'),
    'fonts': os.path.join(CWD, 'res', 'fonts'),
    'configs': os.path.join(CWD, 'res', 'configs'),
    'sketches_a': os.path.join(CWD, 'res', 'images', 'sketches_a'),
    'sketches_b': os.path.join(CWD, 'res', 'images', 'sketches_b'),
}

FILES = {
    'icon': os.path.join(CWD, 'res', 'icons', 'logo.ico'),
    'logo': os.path.join(CWD, 'res', 'images', 'logos', 'apollo_logo.png'),
    'font-stsev': os.path.join(CWD, 'res', 'fonts', 'STSEV851-78.ttf'),
}

RIGHT = 'Вправо' 
LEFT = 'Влево'

NO = 'НЕТ'
YES = 'ДА'

TRIANGLE = 'Треугольная'
RECTANGLE = 'Прямоугольная'

LIGHT = 'Лайт'
PRESTIGE = 'Престиж'
PREMIUM = 'Премиум'
DEALER = 'Дилер'

GUI = {
    'title': 'Откатные ворота "АПОЛЛО"',
    'win_width': 600,
    'win_height': 600,
    'size_text': [20, 1],
    'size_input': [30, 1],
    'size_combo': [27, 1],
    'size_multiline': [45, 5],
    'fonts': {
        'normal': [
            'Calibri',
            '10'
        ],
        'bold': [
            'Calibri',
            '10',
            'bold'
        ]
    }
}

PDF = {
    'creator': 'fpdf'
}

SKETCHES_A = (
    {
        'model': [PRESTIGE, PREMIUM],
        'size': ['a',],
        'side': [LEFT,],
        'console': [TRIANGLE,],
        'filename': 'patl.png'
    },
    {
        'model': [PRESTIGE, PREMIUM],
        'size': ['a',],
        'side': [RIGHT,],
        'console': [TRIANGLE,],
        'filename': 'patr.png'
    },
)


CONSOLE_TYPES = (
    TRIANGLE,
    RECTANGLE
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

BEAM_TYPES = (
    'Без опорной балки',
    'Опорная балка',
    'Продольная закладная'
)

COLUMN_TYPES = (
    'Стандартный',
    'П-образный 100х50'
)

SIDE_TYPES = (
    RIGHT,
    LEFT
)


GATE_MODELS = (
    LIGHT,
    PRESTIGE,
    PREMIUM,
    DEALER
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
    'model': {
        'text': 'Модель ворот',
        'values': GATE_MODELS
    },
    'width': {
        'text': 'Ширина проема, мм',
        'values': None,
        'int': True,
    },
    'full_width': {
        'text': 'Место для отката, мм',
        'values': None,
        'int': True,
    },
    'cliarance': {
        'text': 'Просвет, мм',
        'values': None,
        'int': True,
    },
    'height': {
        'text': 'Высота полотна, мм',
        'values': None,
        'int': True,
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
            YES,
            NO
        )
    },
    'adjustments': {
        'text': 'Рег.площадки',
        'values': (
            YES,
            NO
        )
    },
    'door': {
        'text': 'Встроенная калитка',
        'values': (
            YES,
            NO
        )
    },
    'decor': {
        'text': 'Переменный щит',
        'values': (
            YES,
            NO
        )
    },
    'comments': {
        'values': '>Text<'
    }
}
