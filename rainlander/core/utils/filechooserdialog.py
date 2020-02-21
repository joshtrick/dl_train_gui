import os
import psutil
import sys
import time
import threading
import signal
import subprocess

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty


class FileChooserDialog(FloatLayout):

    select = ObjectProperty(None)
    cancel = ObjectProperty(None)
    text_info = ObjectProperty(None)
    filters = ObjectProperty(None)
    Builder.load_file('ui/utils/filechooserdialog.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass
