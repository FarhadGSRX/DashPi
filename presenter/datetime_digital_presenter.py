
class DateTimeDigitalPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def generate(self):
        dt = self.model.get_current_date_time()
        return self.view.display_datetime(dt)
    