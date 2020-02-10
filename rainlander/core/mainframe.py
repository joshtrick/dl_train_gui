import os
import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ObjectProperty
from core.mainsections.annotatescreen import AnnotateScreen
from core.mainsections.trainscreen import TrainScreen
from core.mainsections.evaluatescreen import EvaluateScreen
from core.mainsections.generatesgscreen import GenerateSGScreen

class MainFrame(GridLayout):
    Builder.load_file('ui/mainframe.kv')

    def __init__(self, **kwargs):
        super(MainFrame, self).__init__(**kwargs)
        app = App.get_running_app()
        pass

    def disable_all_menu_buttons(self):
        for child in self.ids.main_menu_view.children:
            child.disabled = True

    def enable_all_menu_buttons(self):
        for child in self.ids.main_menu_view.children:
            child.disabled = False
