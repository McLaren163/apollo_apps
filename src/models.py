from pymitter import EventEmitter
import csv
import math
from src import config as CFG
from src.exeptions import ApolloError, NotIntError, SmallConsoleError, SketchNotFoundByConditionError
from src.fpdf_creator import PDFShiftgate
from src.utilities import FilterByDict, get_filepath

SMALL_FULL_WIDTH_ATT = 'Размер консоли меньше 1//5 ширины проема!'
SHORT_RACK_ATT = 'Недостаточное количество рубчатой рейки!'

WORK_WIDTH_INCREMENT = 300


class ShiftGateModel(EventEmitter):
    def __init__(self, design_map):
        super().__init__()
        # create empty state
        self.state = {}
        # create empty errors list
        self.errors = []
        # self.change_state = True
        self.design_map = design_map

    def create_draft(self, data):
        self.state = data
        try:
            self.calculate_data()
            self.create_pdf_file(PDFShiftgate, data, data.get('filepath'))
        except ApolloError as e:
            self.emit('errors', *e.get_messages())
        else:
            # send event with new data
            self.emit('ok', self.state.get('filepath'))

    def create_pdf_file(self, pdf_creator, data, filepath):
        pdf_creator(data).save(filepath)

    def calculate_data(self, data=None):
        if data:
            self.state = data
        # add empty attention lists to the model state
        self.state['attentions'] = []
        #  add test attention info
        self._addAttention('This text for test attentions!!!')

        self._validation_for_int()
        self._calc_full_width()
        self._calc_work_width()
        self._calc_console_width()
        self._calc_beam_length()
        self._add_sketch_a()
        self._add_sketch_b()
        self._isAutomatic()

    def _validation_for_int(self):
        bad_params = []

        to_validate = [key for key, value in CFG.WIDGETS.items()
                       if value.get('int')]

        for key in to_validate:
            if not self.state.get(key).isdigit():
                text = CFG.WIDGETS.get(key).get('text')
                bad_params.append(text)

        if bad_params:
            raise NotIntError(*bad_params)

    def _addAttention(self, text):
        self.state['attentions'].append(text)

    def _isAutomatic(self):
        state = self.state
        rack = state.get('rack')
        if not rack.isdigit():
            state['is_automatic'] = False
            return
        state['is_automatic'] = True
        rack = int(rack)
        min_rack = math.ceil((int(state.get('width')) + 500) / 1000)
        if rack < min_rack:
            self._addAttention(SHORT_RACK_ATT)

    def _calc_beam_length(self):
        state = self.state
        full_width = int(state.get('full_width'))
        width = int(state.get('width'))
        state['beam_l'] = str(full_width - width - WORK_WIDTH_INCREMENT//2)

    def _calc_console_width(self):
        state = self.state
        full_width = int(state.get('full_width'))
        work_width = int(state.get('work_width'))
        console_width = full_width - work_width
        state['console_width'] = console_width

    def _calc_work_width(self):
        state = self.state
        work_width = int(state.get('width')) + WORK_WIDTH_INCREMENT
        state['work_width'] = str(work_width)

    def _calc_full_width(self):
        state = self.state
        full_width = int(state.get('full_width'))
        width = int(state.get('width'))
        full_width_min = int(width * 1.3)
        full_width_max = int(width * 1.5)

        if full_width < full_width_min:
            raise SmallConsoleError(full_width)
        elif full_width >= full_width_max:
            state['full_width'] = str(full_width_max)
        else:
            self._addAttention(SMALL_FULL_WIDTH_ATT)

    def _add_sketch_a(self):
        # FIXME 
        filter_ = {}
        filter_['model'] = self.state.get('model')
        filter_['side'] = self.state.get('side')
        filter_['console'] = self.state.get('console')
        filter_['size'] = self._get_size_type(
            self.state.get('model'),
            self.state.get('width'),
            self.state.get('height')
        )
        sketches = FilterByDict(CFG.SKETCHES_A)
        count_of_results = sketches.apply_filter(filter_)
        if count_of_results:
            result = sketches.get_next()
            path = get_filepath(CFG.FOLDERS.get('sketches_a'),
                                result.get('filename'))
            self.state['sketch_a_path'] = path 
        else:
            raise SketchNotFoundByConditionError('A')

    def _add_sketch_b(self):
        pass

    def _get_size_type(self, model, width, height):
        return 'a'

class DesignModelMap():
    def __init__(self, map_file):
        self.map_file = map_file

    def getType(self, width, height):
        with open(self.map_file) as file:
            type_map = csv.DictReader(file, delimiter=';')
            headers = type_map.fieldnames
            col = None
            for header in headers:
                try:
                    if width <= int(header):
                        col = header
                        break
                except Exception as e:
                    pass

            if not col:
                return None

            for row in type_map:
                if height <= int(row['H']):
                    return row[col]
