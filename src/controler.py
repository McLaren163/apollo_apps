class Controler():

    def __init__(self, view, model, start_state=None):
        self.view = view
        self.model = model
        self.subscribeOnEvents()

    def subscribeOnEvents(self):
        self.view.on('submit', self.view_submit)

    def view_submit(self, args):
        print('submit controller')
        args['order'] = '666'
        self.view.setState(args)
