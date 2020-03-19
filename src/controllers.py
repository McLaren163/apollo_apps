class Controller():

    def __init__(self, view, model):
        self.view = view
        self.model = model
        self._subscribe_on_events()

    def start(self, start_state=None):
        self.view.run(state=start_state)

    def _subscribe_on_events(self):
        self.view.on('submit', self.submit_handler)

        self.model.on('errors', self.errors_handler)
        self.model.on('ok', self.show_result_handler)

    def submit_handler(self, data):
        self.model.create_draft(data)

    def errors_handler(self, *errors):
        self.view.show_errors(*errors)

    def show_result_handler(self, filepath):
        self.view.show_result(filepath)
