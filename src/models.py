from pymitter import EventEmitter
import csv


class ShiftGateModel(EventEmitter):

    def __init__(self, validator, design_map):
        super().__init__()
        self.state = {}
        self.change_state = True
        # validator.resetState(self.state)
        # self.validator = validator
        self.design_map = design_map

    def setState(self, props):
        self.state.update(props)
        # проверить новое значение и внести корректировки в существующие
        self.change_state = True
        self.emit('new state', self.state.copy())

    def startCalculate(self):
        if self.change_state:
            data = self.calcFullData()
            self.state.update(data)
            self.change_state = False
        self.emit('return data', self.state.copy())

    def getFType(self):
        return None #FIXME

    def getSType(self):
        frame = self.getFrameType(self.state['width'], self.state['height'])
        console = self.getConsoleType(self.state['console'])
        side = self.getSideType(self.state['side'])
        return (frame + console + side).upper()

    def getSideType(self, side):
        if side == 'Влево':
            return 'L'
        elif side == 'Вправо':
            return 'R'
        else:
            return None

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

    def calcFullData(self):
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

        s_type = self.getSType()
        if s_type:
            new_data.update({'s_type': s_type})

        f_type = self.getFType()
        if f_type:
            new_data.update({'f_type': f_type})

        slices = self.calcSlices(s_type) # dict {тип трубы: длина куска}

        weight_gate = self.calcWeightGate(slices)
        weight_filling = self.calcWeightFilling(self.state.get('filling'))
        full_weight = weight_filling + weight_gate

        new_data['attention'] = attentions
        return new_data

    def calcSlices(self, design_type):
        return {} #FIXME

    def calcWeightGate(self, slices):
        return 0 #FIXME

    def calcWeightFilling(self, filling_type):
        return 0 #FIXME



    # def isValid(self, props):
    #     """Проверяет данные на валидность"""
    #     id, value = list(props.items())[0]
    #     print('isValid props:', id, value)
    #     res = self.validator.checkValue(id, value)
    #     print('isValid result:', res)
    #     if res:
    #         self.emit('errors', res)


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
