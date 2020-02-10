import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class EvaluateScreen(Screen):
    Builder.load_file('ui/mainsections/evaluatescreen.kv')

    def __init__(self, **kwargs):
        super(EvaluateScreen, self).__init__(**kwargs)
        pass

