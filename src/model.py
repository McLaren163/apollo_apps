from pymitter import EventEmitter
import csv


class Model(EventEmitter):

    def __init__(self, model_map):
        super().__init__()
        self.model_map = model_map
        self.state = {}

    def setState(self, props):
        self.state.update(props)

    def getType(self):
        return self.model_map.getType(int(self.state['width']),
                                      int(self.state['height']))

    def getDrawings(self):
        pass

    def getComposition(self):
        pass

    def isValid(self, props):
        """Проверяет данные на валидность"""
        bad_props = {}
        ids = ('width', 'height', 'cliarance')
        for id in ids:
            if id in props:
                try:
                    int(props[id])
                except:
                    bad_props[id] = 'ОШИБКА'
        if bad_props:
            self.emit('bad props', bad_props)


class ModelMap():

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
        return None
