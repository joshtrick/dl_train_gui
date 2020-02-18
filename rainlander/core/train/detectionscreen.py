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
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

from core.utils.filechooserdialog import FileChooserDialog
from utils.dummy import dummy_func

class DetectionScreen(Screen):

    Builder.load_file('ui/train/detectionscreen.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    # ********Functions for File Chooser Dialog********
    def show_filechosser(self, text_input_id, choose_path = False):
        if choose_path:
            title = "Path Seclector"
            content = FileChooserDialog(
                    select = self.select_path,
                    cancel = self.dismiss_filechooser,
                    text_info = self.ids[text_input_id])
        else:
            title = "File Seclector"
            content = FileChooserDialog(
                    select = self.select_file,
                    cancel = self.dismiss_filechooser,
                    text_info = self.ids[text_input_id])
        self._popup = Popup(
                title = title,
                content = content,
                size_hint = (0.9, 0.9))
        self._popup.open()

    def dismiss_filechooser(self):
        self._popup.dismiss()

    def select_file(self, path, filename, text_info):
        try:
            text_info.text = filename[0]
        except:
            print("No file selected!")
            pass
        self.dismiss_filechooser()

    def select_path(self, path, filename, text_info):
        print(path)
        text_info.text = path
        self.dismiss_filechooser()



    # ********Functions for Training********
    def train(self):
        print(self.ids.model_selector.text)
        print(self.ids.parameter01.value)
        print(self.ids.parameter02.text)
        print(self.ids.filepath01.text)
        print(self.ids.folderpath01.text)
        #dummy_func(100)
        #os.system("gnome")
        #os.system("gnome-terminal -x python utils/dummy.py")
        #self.pro = subprocess.Popen(['python', 'utils/dummy.py'])

    def stop(self):
        try:
            self.pro.terminate()
        except:
            pass
        #os.killpg(os.getpgid(self.pro.pid), signal.SIGTERM)

