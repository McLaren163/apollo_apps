from pymitter import EventEmitter
import csv


class Model(EventEmitter):

    def __init__(self, model_map):
        self.model_map = model_map
        self.state = {}

    def setState(self, values):
        self.state.update(values)

    def getType(self):
        return self.model_map.getType(int(self.state['width']),
                                      int(self.state['height']))

    def getDrawings(self):
        pass

    def getComposition(self):
        pass


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
                except:
                    pass

            if not col:
                return None

            for row in type_map:
                if height <= int(row['H']):
                    return row[col]
        return None
