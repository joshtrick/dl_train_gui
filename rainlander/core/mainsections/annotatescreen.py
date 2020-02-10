import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class AnnotateScreen(Screen):
    Builder.load_file('ui/mainsections/annotatescreen.kv')

    def __init__(self, **kwargs):
        super(AnnotateScreen, self).__init__(**kwargs)
        pass

    def create_labelme_thread(self):
        self.run_labelme_t = threading.Thread(target = self.run_labelme)

    def run_labelme(self):
        self.ids.run_labelme_btn.disabled = True
        os.system('labelme')
        self.ids.run_labelme_btn.disabled = False
