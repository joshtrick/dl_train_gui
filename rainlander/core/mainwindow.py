from kivy.app import App
from core.mainframe import MainFrame

class MainWindowApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_frame = MainFrame()

    def build(self):
        return self.main_frame
