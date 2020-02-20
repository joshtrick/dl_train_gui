import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

from core.utils.filechooserdialog import FileChooserDialog
from utils.label_collector import label_collector

class AnnotateScreen(Screen):
    Builder.load_file('ui/mainsections/annotatescreen.kv')

    def __init__(self, **kwargs):
        self.run_func_t = None
        super().__init__(**kwargs)
        pass

    def create_func_thread(self, func):
        self.run_func_t = threading.Thread(target = func)

    def run_labelme(self):
        self.disable_group_buttons(self.ids.main_pannel)
        os.system('labelme')
        self.enable_group_buttons(self.ids.main_pannel)

    def run_class_generator(self):
        self.disable_group_buttons(self.ids.main_pannel)
        label_collector(self.ids.param_dataset_path.text)
        self.enable_group_buttons(self.ids.main_pannel)

    def disable_group_buttons(self, id):
        for child in id.children:
            if isinstance(child, Button):
                child.disabled = True

    def enable_group_buttons(self, id):
        for child in id.children:
            if isinstance(child, Button):
                child.disabled = False

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
