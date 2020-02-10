import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from core.train.segmentationscreen import SegmentationScreen
from core.train.detectionscreen import DetectionScreen
from core.train.classificationscreen import ClassificationScreen

class TrainScreen(Screen):
    Builder.load_file('ui/mainsections/trainscreen.kv')

    def __init__(self, **kwargs):
        super(TrainScreen, self).__init__(**kwargs)
        pass

