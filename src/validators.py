class Validator():

    def __init__(self):
        self.checkers = {
            'order': self._isEmpty,
            'engineer': self._isEmpty,
            'customer': self._isEmpty,
            'date': self._checkDate,
            'width': self._checkWidth
        }
        self.resetState()

    def resetState(self, modelState={}):
        self.modelState = modelState

    def applyNewValue(self, id, value):
        self.modelState[id] = value

    def checkValue(self, id, value):
        checkFunc = self.checkers.get(id, (lambda id, val: None))
        res = checkFunc(id, value)
        print('modelState:', self.modelState)
        ### тут все ne verno
        return res

    def _isEmpty(self, id, value):
        if not value:
            return {id: 'ВВЕДИТЕ'}

    def _isInt(self, id, value):
        try:
            intvalue = int(value)
        except ValueError as e:
            return {id: 'ВВЕДИТЕ ЧИСЛО'}
        else:
            return None

    def _checkDate(self, id, value):
        if self.modelState.get('order'):
            return {id: 'set date'}

    def _checkWidth(self, id, value):
        res = self._isInt(id, value)
        if not res:
            full_width = int(int(value) * 1.5)
            self.modelState['full_width'] = full_width
            return {'full_width': full_width}
        else:
            return res


if __name__ == '__main__':
    v = Validator().checkValue('order', '')
    print(v)
