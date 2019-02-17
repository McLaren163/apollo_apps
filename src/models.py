from pymitter import EventEmitter
import csv


class ShiftGateModel(EventEmitter):

    def __init__(self, validator, design_map):
        super().__init__()
        self.state = {}
        # validator.resetState(self.state)
        # self.validator = validator
        self.design_map = design_map

    def setState(self, props):
        self.state.update(props)
        self.emit('new state', self.state.copy())

    def getDesignType(self, width, height):
        """
        вернет тип конструктива рамы,
        если не найдет, то вернет None
        """
        return self.design_map.getType(int(width),
                                      int(height))

    def getShiftType(self, shift_value):
        """
        вернет тип стороны отката,
        если не найдет, то вернет None
        """
        if shift_value == 'Влево':
            return 'L'
        elif shift_value == 'Вправо':
            return 'R'

    def calcFullData(self):
        """
        вернет полные данные о модели для представления
        data: {
            sideType: str # тип чертежа 'АЛ' (А-тип Л-сторона)
            frontType: str # тип чертежа 'A'
            slices: dict # нарезка металла
            ... # значения параметров
            attention: tupl # список предупреждений
        }
        """
        data = {}
        desing_type = self.getDesignType(self.state.get('width'),
                                         self.state.get('height')) or ''
        shift_type = self.getShiftType(self.state.get('side')) or ''
        data['sideType'] = desing_type + shift_type
        data['frontType'] = '' # FIXME
        slices = self.calcSlices(desing_type) # dict {тип трубы: длина куска}
        weight_gate = self.calcWeightGate(slices)
        weight_filling = self.calcWeightFilling()



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
