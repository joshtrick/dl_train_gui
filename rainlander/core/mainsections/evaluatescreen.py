import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

from core.utils.filechooserdialog import FileChooserDialog

class EvaluateScreen(Screen):
    Builder.load_file('ui/mainsections/evaluatescreen.kv')

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

    # ********Functions for Evaluation********
    def load_preview(self):
        try:
            self.ids.img_display.source = self.ids.file_tree.selection[0]
        except:
            return

    def load_result(self):
        try:
            img_path = self.ids.file_tree.path
            file_name = os.path.basename(self.ids.file_tree.selection[0])
            ret_file_path = os.path.join(img_path, "rl_results", file_name)
            print(ret_file_path)
        except:
            print("Invalid input file")
        else:
            if os.path.exists(ret_file_path):
                self.ids.ret_display.source = ret_file_path
            else:
                try:
                    self.evaluate(img_path, file_name)
                except:
                    pass

    def evaluate(self, img_path, file_name):
        ret_file_path = os.path.join(img_path, "rl_results", file_name)
        print("evaluate")
        time.sleep(5)
        print("done")
        self.ids.ret_display.source = ret_file_path
        print(ret_file_path)
