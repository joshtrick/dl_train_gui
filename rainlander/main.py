import kivy
kivy.require('1.11.1')
from kivy.core.window import Window

import sys
sys.path.append(".")

from core.mainwindow import MainWindowApp

def main():
    Window.size = (960, 540)
    MainWindowApp(title = "RainLander").run()

if __name__ == '__main__':
    main()
