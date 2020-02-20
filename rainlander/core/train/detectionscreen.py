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
from crtrain.protos.pipeline_pb2 import TrainPipeLine

from core.utils.filechooserdialog import FileChooserDialog
from utils.dummy import dummy_func

class DetectionScreen(Screen):

    Builder.load_file('ui/train/detectionscreen.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.train_process = None
        self.param_dict = {}
        self.alias_dict = {
                'Detection'         : "detector",
                'Segmentation'      : "segmentation_model",
                'Classification'    : "classification_model",
                'Tiny-Yolo'         : "yolo"
                }
        Clock.schedule_once(self.param_init, 0)
    # ********Parameters Registry********
    def param_init(self, dt = 0):
        self.param_update()
        self.param_print()

    def param_update(self):
        self.param_dict['model_type']                   = self.alias_dict[self.ids.param_model_type.text]
        self.param_dict['model_name']                   = self.alias_dict[self.ids.param_model_selector.text]
        self.param_dict['num_classes']                  = int(self.ids.param_num_classes.text)
        self.param_dict['gpus']                         = self.ids.param_gpus.text
        self.param_dict['checkpoint_path']              = os.path.join(self.ids.param_checkpoint_path.text, 'ckpt')
        self.param_dict['train_dir']                    = self.ids.param_train_dir.text
        self.param_dict['encrypted_initial_checkpoint'] = self.ids.param_encrypted_initial_checkpoint.active
        self.param_dict['batch_size']                   = self.ids.param_batch_size.value
        self.param_dict['input_sizes']                  = [int(self.ids.param_input_w.text), int(self.ids.param_input_h.text)]
        self.param_dict['class_name_path']              = self.ids.param_class_name_path.text
        self.param_dict['image_dir']                    = self.ids.param_image_dir.text
        self.param_dict['label_path']                   = self.ids.param_label_path.text
        self.param_dict['random_translate']             = self.ids.param_random_translate.active
        self.param_dict['random_crop']                  = self.ids.param_random_crop.active
        self.param_dict['random_horizontal_flip']       = self.ids.param_random_horizontal_flip.active
        self.param_dict['random_vertical_flip']         = self.ids.param_random_vertical_flip.active
        self.param_dict['random_rotation']              = self.ids.param_random_rotation.active
        self.param_dict['random_shuffle_channel']       = self.ids.param_random_shuffle_channel.active
        self.param_dict['gray']                         = self.ids.param_gray.active

    def write_config(self):
        tep = TrainPipeLine()  # 训练pipeline

        tep.model.detector.yolo.num_classes             = self.param_dict['num_classes']
        tep.model.detector.yolo.model_scale             = 0  # yolo 目前只有一个版本
        tep.train_config.gpus                           = self.param_dict['gpus']
        tep.train_config.checkpoint_path                = self.param_dict['checkpoint_path']
        tep.train_config.train_dir                      = self.param_dict['train_dir']
        tep.train_config.encrypted_initial_checkpoint   = self.param_dict['encrypted_initial_checkpoint']
        tep.reader.batch_size                           = self.param_dict['batch_size']
        tep.reader.class_name_path                      = self.param_dict['class_name_path']
        tep.reader.input_sizes.extend(self.param_dict['input_sizes'])
        tep.reader.image_input_reader.label_path        = self.param_dict['label_path']
        tep.reader.image_input_reader.image_dir         = self.param_dict['image_dir']

        tep.reader.preprocessing.random_translate       = self.param_dict['random_translate']
        tep.reader.preprocessing.random_crop            = self.param_dict['random_crop']
        tep.reader.preprocessing.random_horizontal_flip = self.param_dict['random_horizontal_flip']
        #tep.reader.preprocessing.random_vertical_flip   = self.param_dict['random_vertical_flip']
        #tep.reader.preprocessing.random_rotation        = self.param_dict['random_rotation']
        #tep.reader.preprocessing.random_shuffle_channel = self.param_dict['random_shuffle_channel']
        #tep.reader.preprocessing.gray                   = self.param_dict['gray']

        # 序列化该配置为文本文件(config)
        with open("workspace/config_tmp/train.config", 'w') as fp:
          fp.write(text_format.MessageToString(tep))


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

    # ********Functions for Training********
    def set_config(self):
        self.param_update()
        #self.param_print()
        self.write_config()
        pass

    def train(self):
        self.set_config()
        if self.train_process == None:
            self.train_process = subprocess.Popen(['python', 'utils/run_config.py'])
        else:
            print("Already running")

    def stop(self):
        try:
            self.train_process.kill()
            self.train_process = None
        except:
            pass

