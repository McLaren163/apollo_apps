from pymitter import EventEmitter
import csv

SMALL_CONSOLE_ERR = 'Размер консоли меньше 1//3 ширины проема'
NOT_DRAFT_ERR = 'Нет подходящего типа чертежа'


class ShiftGateModel(EventEmitter):
    def __init__(self, design_map):
        super().__init__()
        # create empty state
        self.state = {}
        # create empty errors list
        self.errors = []
        # self.change_state = True
        self.design_map = design_map

    # def setState(self, props):
    #     self.state.update(props)
    #     # проверить новое значение и внести корректировки в существующие
    #     self.change_state = True
    #     self.emit('new state', self.state.copy())

    def calculate(self, data):
        # clear model state
        self.state.clear()
        # update model state with external data
        self.state.update(data)
        # add empty attention lists to the model state
        self.state['attentions'] = []
        # add draft type to the model state
        self._addDraftTypeToState(self.state)
        self._calcFullWidth(self.state)
        self._calcWorkWidth(self.state)
        self._calcConsoleWidth(self.state)

        # send event with new data
        self.emit('return data', self.state)

    def _calcConsoleWidth(self, state):
        full_width = int(state.get('full_width'))
        work_width = int(state.get('work_width'))
        console_width = full_width - work_width
        state['console_width'] = console_width

    def _calcWorkWidth(self, state):
        work_width = int(state.get('width')) + 300
        state['work_width'] = work_width

    def _calcFullWidth(self, state):
        full_width = int(state.get('full_width', 0))
        width = int(state.get('width'))
        width_min = int(width * 1.3)
        width_max = int(width * 1.5)

        if full_width < width_min:
            self.errors.append(SMALL_CONSOLE_ERR)
            self.emit('errors', self.errors)
        if full_width >= width_max:
            full_width = width_max

        state['full_width'] = full_width

    def _addDraftTypeToState(self, state):
        draft_type = self.getDraftType(state)
        if draft_type:
            state['draft_type'] = draft_type
        else:
            self.errors.append(NOT_DRAFT_ERR)

    def getFType(self, values):
        return None  # FIXME

    def getDraftType(self, data):
        frame = self.getFrameType(data['width'], data['height'])
        console = self.getConsoleType(data['console'])
        direction = self.getDirectionType(data['side'])
        return (frame + console + direction).upper()

    def getDirectionType(self, direction):
        if direction == 'Влево':
            return 'L'
        elif direction == 'Вправо':
            return 'R'
        else:
            return '_'

    def getConsoleType(self, console):
        if console == 'Треугольная':
            return 'T'
        elif console == 'Прямоугольная':
            return 'P'
        else:
            return None

    def getFrameType(self, width, height):
        """
        вернет тип конструктива рамы,
        если не найдет, то вернет None
        """
        return self.design_map.getType(int(width),
                                       int(height))

    def calcFullData(self, values):
        """
        вернет полные данные о модели для представления
        data: {
            sideType: str # тип чертежа 'АЛ' (А-тип Л-сторона)
            frontType: str # тип чертежа 'A'
            slices: dict # нарезка металла
            ... # значения параметров
            attention: list # список предупреждений
        }
        """
        new_data = {}
        attentions = []

        # тип чертежа вид содвора
        s_type = self.getSType(values)
        if s_type:
            new_data['s_type'] = s_type

        # тип чертежа вид сбоку
        f_type = self.getFType(values)
        if f_type:
            new_data['f_type'] = f_type

        # нарезка металла
        slices = self.calcSlices(s_type)  # dict {тип трубы: длина куска}

        # основные размеры чертежа
        main_sizes = self.getMainSizes(values)
        new_data['main_sizes'] = main_sizes

        # вес составляющих ворот
        weight_gate = self.calcWeightGate(slices)
        weight_filling = self.calcWeightFilling(self.state.get('filling'))
        weight_bus = self.calcWeightBus()
        weight_without_bus = weight_filling + weight_gate
        new_data['weight_without_bus'] = weight_without_bus
        full_weight = weight_without_bus + weight_bus
        new_data['full_weight'] = full_weight

        new_data['attention'] = attentions
        return new_data

    def getMainSizes(self, values):
        return None # FIXME

    def calcSlices(self, design_type):
        return {}  # FIXME

    def calcWeightGate(self, slices):
        return 0  # FIXME

    def calcWeightFilling(self, filling_type):
        return 0  # FIXME


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
