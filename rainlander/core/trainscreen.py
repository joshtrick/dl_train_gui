import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class TrainScreen(Screen):
    Builder.load_file('ui/trainscreen.kv')

    def __init__(self, **kwargs):
        super(TrainScreen, self).__init__(**kwargs)
        pass

