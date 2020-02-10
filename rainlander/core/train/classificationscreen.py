import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class ClassificationScreen(Screen):
    Builder.load_file('ui/train/classificationscreen.kv')

    def __init__(self, **kwargs):
        super(ClassificationScreen, self).__init__(**kwargs)
        pass
