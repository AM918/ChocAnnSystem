# A window abstraction class written for the final project for COMP370.

# Need this to init QApplication
import sys

# Basic system checks
if sys.version_info[0] < 3 or sys.version_info[1] < 5:
    raise SystemError("Your version of Python is out of date.\nPlease use Python 3.")

# Basic required widgets
from PyQt5.QtWidgets import QWidget, QPushButton
# All interfaces required for instantiation
from interface import Interface, ProviderInterface, OperatorInterface, ManagerInterface
# Database
from database_manager import DatabaseManager

class window(QWidget): 
    """A window class, very simple, just for the main selection window."""
    def __init__(self):
        """Does basic window setup."""
        super().__init__() # Must explicitly call super's constructor if overriding (when inheriting from QWidget)

        # Create the database
        self.db = DatabaseManager()

        # Create the interfaces
        self.init_interfaces()

        # Create the layout for the window
        self.init_buttons()

        # Do basic window setup
        self.resize(400, 400)
        self.setWindowTitle("COMP370 Project")
        self.show() # Necessary

    def quit_function(self):
        """Quits the entire application after saving."""
        self.db.saveClients()
        sys.exit(0)

    def show_manager(self):
        """Shows the manager interface."""
        self.m_interface.show()

    def show_provider(self):
        """Shows the provider interface."""
        self.p_interface.show()

    def show_operator(self):
        """Shows the operator interface."""
        self.o_interface.show()

    def init_interfaces(self):
        """Creates the interfaces.
        Works on a simple pattern -
        Create the interface as a member of self,
        hide the interface,
        add the database to the interface for use.
        """
        self.p_interface = ProviderInterface(None)
        self.p_interface.hide()
        self.p_interface.addDB(self.db)
        self.m_interface = ManagerInterface(None)
        self.m_interface.hide()
        self.m_interface.addDB(self.db)
        self.o_interface = OperatorInterface(None)
        self.o_interface.hide()
        self.o_interface.addDB(self.db)

    def init_buttons(self):
        """Creates the layout of the main window screen."""
        quit_button = QPushButton('Quit', self) # Quits the application
        quit_button.clicked.connect(self.quit_function)
        quit_button.move(10, 330)

        o_button = QPushButton('Operator Interface', self)
        o_button.clicked.connect(self.show_operator)
        o_button.move(10, 30)

        p_button = QPushButton('Provider Interface', self)
        p_button.clicked.connect(self.show_provider)
        p_button.move(10, 130)

        m_button = QPushButton('Manager Interface', self)
        m_button.clicked.connect(self.show_manager)
        m_button.move(10, 230)

        quit_button.setFixedSize(380, 50)
        o_button.setFixedSize(380, 50)
        p_button.setFixedSize(380, 50)
        m_button.setFixedSize(380, 50)