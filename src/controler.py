class Controler():

    def __init__(self, view, model, start_state=None):
        self.view = view
        self.model = model
        self.subscribeOnEvents()

    def subscribeOnEvents(self):
        self.view.on('submit', self.view_submit_handler)

    def view_submit_handler(self, args):
        print('submit controller')
        self.model.setState(args)
        print('Model type: {}'.format(self.model.getType()))
        args['order'] = '666'
        self.view.setState(args)
