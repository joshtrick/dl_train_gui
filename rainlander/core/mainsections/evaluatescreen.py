import os
import psutil
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class EvaluateScreen(Screen):
    Builder.load_file('ui/mainsections/evaluatescreen.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

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
