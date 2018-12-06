class Controler():

    def __init__(self, view, model, start_state=None):
        self.view = view
        self.model = model
        self.subscribeOnEvents()

    def subscribeOnEvents(self):
        self.view.on('submit', self.view_submit_handler)
        self.model.on('bad props', self.model_bad_values)
        self.model.on('new props', self.view.setState)

    def view_submit_handler(self, args):
        print('submit controller')
        self.model.isValid(args)

    def model_bad_values(self, args):
        print('bad props controller')
        self.view.setState(args)
