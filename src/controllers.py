class Controller():

    def __init__(self, view, model, start_state=None):
        self.view = view
        self.model = model
        self.subscribeOnEvents()

    def subscribeOnEvents(self):
        self.view.on('submit', self.submitHandler)
        self.view.on('new value', self.newValuesHandler)

        self.model.on('new state', self.syncViewHandler)
        self.model.on('errors', self.errorsHandler)
        self.model.on('return data', self.returnDataHandler)

    def submitHandler(self):
        self.model.startCalculate()

    def newValuesHandler(self, args):
        self.model.setState(args)

    def errorsHandler(self, args):
        pass

    def syncViewHandler(self, args):
        self.view.setState(args)

    def returnDataHandler(self, args):
        self.view.showResult(args)
