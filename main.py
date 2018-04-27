"""
This is a basic main application 'bootstrap' script.

It creates the application and the main window. Fairly self-explanatory code.
"""

import sys
import main_window 
from deb import debp, errp
from PyQt5.QtWidgets import QApplication

def main():
    """This goes to the main view"""
    debp('Creating application.')
    a = QApplication(sys.argv)

    debp('Creating window.')
    window = main_window.window()

    debp('Launching application.')
    sys.exit(a.exec_()) # Special 'qt' way of launching application.

if __name__ == '__main__':
    main() 
