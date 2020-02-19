import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from core.train.segmentationscreen import SegmentationScreen
from core.train.detectionscreen import DetectionScreen
from core.train.classificationscreen import ClassificationScreen

class TrainScreen(Screen):
    Builder.load_file('ui/mainsections/trainscreen.kv')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def disable_group_buttons(self, id):
        for child in id.children:
            if isinstance(child, Button):
                child.disabled = True
        self.ids.cancel.disabled = False

    def enable_group_buttons(self, id):
        for child in id.children:
            if isinstance(child, Button):
                child.disabled = False

    def create_training_thread(self):
        self.start_training_t = threading.Thread(target = self.start_training)

    def start_training(self):
        self.disable_group_buttons(self.ids.button_grid)
        cur_id = self.ids.training_panel_mgr.current
        self.ids[cur_id].train()
        self.enable_group_buttons(self.ids.button_grid)
