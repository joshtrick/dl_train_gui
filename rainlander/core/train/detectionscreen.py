import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class DetectionScreen(Screen):
    Builder.load_file('ui/train/detectionscreen.kv')

    def __init__(self, **kwargs):
        super(DetectionScreen, self).__init__(**kwargs)
        pass
