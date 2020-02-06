import kivy
kivy.require('1.11.1')

import sys
sys.path.append(".")

from core.mainwindow import MainWindowApp

def main():
    MainWindowApp(title = "RainLander").run()

if __name__ == '__main__':
    main()
