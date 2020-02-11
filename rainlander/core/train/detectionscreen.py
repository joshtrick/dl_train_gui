import os
import psutil
import sys
import time
import threading
import signal
import subprocess

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from utils.dummy import dummy_func

class DetectionScreen(Screen):

    Builder.load_file('ui/train/detectionscreen.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    def train(self):
        print("hello")
        #dummy_func(100)
        #os.system("gnome")
        self.pro = subprocess.Popen(['python', 'utils/dummy.py'])

    def stop(self):
        try:
            self.pro.terminate()
        except:
            pass
        #os.killpg(os.getpgid(self.pro.pid), signal.SIGTERM)

