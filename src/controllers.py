class Controller():

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.subscribeOnEvents()

    def start(self, start_state=None):
        self.view.run(state=start_state)

    def subscribeOnEvents(self):
        self.view.on('submit', self.viewSubmitHandler)

        self.model.on('errors', self.errorsHandler)
        self.model.on('return data', self.returnDataHandler)

    def viewSubmitHandler(self, values):
        self.model.calculate(values)

    def errorsHandler(self, errors):
        self.view.showErrors(errors)

    def returnDataHandler(self, data):
        self.view.showResult(data)
