import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class SegmentationScreen(Screen):
    Builder.load_file('ui/train/segmentationscreen.kv')

    def __init__(self, **kwargs):
        super(SegmentationScreen, self).__init__(**kwargs)
        pass
