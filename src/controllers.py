class Controller():

    def __init__(self, view, model, start_state=None):
        self.view = view
        self.model = model
        self.subscribeOnEvents()

    def subscribeOnEvents(self):
        self.view.on('submit', self.submitHandler)
        self.view.on('new value', self.checkValuesHandler)

        self.model.on('new state', self.syncViewModelHandler)
        self.model.on('errors', self.errorsHandler)

    def submitHandler(self, args):
        self.model.isValid(args)

    def checkValuesHandler(self, args):
        self.model.isValid(args)

    def errorsHandler(self, args):
        pass

    def syncViewModelHandler(self, args):
        self.view.setState(args)
