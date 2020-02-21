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
from kivy.clock import Clock

from google.protobuf import text_format
from crtrain.protos.pipeline_pb2 import EvalPipeLine

from core.utils.filechooserdialog import FileChooserDialog

class EvaluateScreen(Screen):
    Builder.load_file('ui/mainsections/evaluatescreen.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_dict = {}
        self.eval_process = None
        Clock.schedule_once(self.param_init, 0)

    # ********Parameters Registry********
    def param_init(self, dt = 0):
        self.param_update()
        #self.param_print()

    def toggle_btn_text(self, toggle_btn_id, text):
        if self.ids[toggle_btn_id].state == 'down':
            return text
        else:
            return ""

    def param_update(self):
        self.param_dict['model_type']                   = self.toggle_btn_text('det_selector', 'detection') \
                                                        + self.toggle_btn_text('cls_selector', 'classification') \
                                                        + self.toggle_btn_text('seg_selector', 'segmentation')
        self.param_dict['model_name']                   = self.toggle_btn_text('det_selector', self.ids.det_selector.text) \
                                                        + self.toggle_btn_text('cls_selector', self.ids.cls_selector.text) \
                                                        + self.toggle_btn_text('seg_selector', self.ids.seg_selector.text)
        self.param_dict['num_classes']                  = int(self.ids.param_num_classes.text)
        self.param_dict['gpus']                         = self.ids.param_gpus.text
        self.param_dict['checkpoint_path']              = self.ids.param_checkpoint_path.text
        self.param_dict['encrypted_initial_checkpoint'] = self.ids.param_encrypted_initial_checkpoint.active
        self.param_dict['batch_size']                   = self.ids.param_batch_size.value
        self.param_dict['input_sizes']                  = [int(self.ids.param_input_w.text), int(self.ids.param_input_h.text)]
        self.param_dict['class_name_path']              = self.ids.param_class_name_path.text
        self.param_dict['image_dir']                    = self.ids.param_image_dir.text
        self.param_dict['min_score_threshold']          = self.ids.param_min_score_threshold.value

    def write_config(self):
        # Create fodlers and strings
        output_txt_name = os.path.join(self.param_dict['image_dir'], "prediction.txt")
        output_img_path = os.path.join(self.param_dict['image_dir'], "rl_results")
        eval_config_path = os.path.join(self.param_dict['image_dir'], "eval.config")
        try:
            os.makedirs(output_img_path)
        except:
            pass

        # Create pipeline
        pipe = EvalPipeLine()

        pipe.model.detector.yolo.num_classes            = self.param_dict['num_classes']
        pipe.model.detector.yolo.model_scale            = 0  # yolo 目前只有一个版本
        pipe.test_config.gpus                           = self.param_dict['gpus']
        pipe.test_config.min_score_threshold            = self.param_dict['min_score_threshold']
        pipe.test_config.checkpoint_path                = self.param_dict['checkpoint_path']
        pipe.test_config.prediction_export_path         = output_txt_name
        pipe.test_config.image_export_dir               = output_img_path

        pipe.test_reader.batch_size                     = self.param_dict['batch_size']
        pipe.test_reader.class_name_path                = self.param_dict['class_name_path']
        pipe.test_reader.input_sizes.extend(self.param_dict['input_sizes'])
        pipe.test_reader.image_input_reader.image_dir = self.param_dict['image_dir']

        with open(eval_config_path, 'w') as fp:
          fp.write(text_format.MessageToString(pipe))
        return eval_config_path

    def param_print(self):
        print("--------Parameters List--------")
        for key in self.param_dict:
            print(key + ": " + str(self.param_dict[key]))
        print("--------Parameters List--------")

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

    # ********Functions for Image Loading********
    def load_preview(self):
        try:
            self.ids.img_display.source = self.ids.file_tree.selection[0]
        except:
            return

    def load_results(self):
        try:
            img_path = self.ids.file_tree.path
            file_name = os.path.basename(self.ids.file_tree.selection[0])
            ret_file_path = os.path.join(img_path, "rl_results", file_name)
            if os.path.exists(ret_file_path):
                self.ids.ret_display.source = ret_file_path
        except:
            pass

    # ********Functions for Evaluation********
    def set_config(self):
        self.param_update()
        #self.param_print()
        return self.write_config()

    def evaluate(self):
        if self.eval_process == None:
            input_configuration = self.set_config()
            self.eval_process = subprocess.Popen([ \
                    'python', \
                    'utils/run_config.py', \
                    '-t', 'eval', \
                    '-i', input_configuration])
        else:
            print("Already running")
            self.eval_process.kill()
            self.eval_process = None


    def stop(self):
        try:
            self.train_process.kill()
            self.train_process = None
        except:
            pass
