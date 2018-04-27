"""
This module contains relevant classes and methodsto the interfaces used for this project.

Notably, it implements:

- An Interface base class
- A ProviderInterface class which takes care of the Provider's terminal abstraction
- An OperatorInterface class which takes care of the normal operator operations.
- A ManagerInterface class which handles simulation of the manager's interface.
"""

"""
In the interest of full clarity, I should state here that the rest of this file is not well-commented.

The main reason for this is that my hands are in some pain now from writing so much Qt GUI functionality.

I'll try to summarize this file and its functionality.

The ProviderInterface is the first interface I worked on, it took by far the longest and is definitely the ugliest.
Its functionality is not simple, but commenting wouldn't really help that much due to how convoluted it got.
It accomplishes what the provider interface is meant to accomplish, at least, and does it decently well.

The OperatorInterface class is fairly beautiful as I started it much later on, with a better understanding of Qt
and how one might go around creating a nice class. (Although it seems like some sort of stylesheet/templating system
might be what Qt is actually supposed to be used by)
Its setupUI function does all the UI setup in nice, easy, steps. All gen_ functions generate parts of the UI,
whether it be buttons or widgets or layouts.
The buttons are mostly bound to simple imperative functions reading like "edit_m" or "delete_prov" which accomplish
their functionality well.

The ManagerInterface class is simple and works fine, as it only takes care of a simple bit of functionality to do with
the ReportGeneration class.

I really, really, recommend not trying to read through or parse this series of classes. Some of the nicer parts 
may look nice, but they really aren't that nice, and there were just so many variables to create my naming
conventions died a terrible, undeserved death.
- Michael Bennett

"""

from report import ReportGeneration
import database_manager
from provider_directory import ProviderDirectory
from billing_controller import BillingController
import sys
import deb
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QGridLayout, 
    QLabel, 
    QLineEdit,
    QPushButton,
    QStackedWidget
)

class Interface(QStackedWidget):
    """
    Interface is the base class inherited by all interfaces.
    It is used to conduct the basic operations necessary to create a simple interface.
    """

    def __init__(self, parent):
        """A basic init function that requires a parent, as interfaces are not meant to be used on their own."""
        super().__init__(parent) # This instantiates the superclass QWidget with a parent
        self.setupUI() # This does the necessary extra UI setup, generally overloaded by subclasses but still called.

    def setupUI(self):
        # Creates the layout for the interface.
        # A layout (essentially) is a 'scene' of a specific setup of widgets.
        self.layout = QGridLayout()
        self.layout.setSpacing(15)

class ProviderInterface(Interface):
    
    def setupUI(self):
        # This adds everything to the interface that we always want. See Interface.setupUI
        super().setupUI()

        self.pd = ProviderDirectory()
        self.billing = False

        # We now have a layout, and we can add whatever we want to it.
        # This is the provider interface, so we want them to enter their provider number.
        num_prompt = QLabel('Enter Provider Number')
        self.prompt_font = num_prompt.font()
        self.prompt_font.setPointSize(24)
        num_prompt.setFont(self.prompt_font)

        self.num_input = QLineEdit()
        # Nine digits only - this allows for that
        # Note - there does appear to be a slight bug with this as detailed here:
        # http://www.qtcentre.org/threads/7106-QLineEdit-and-input-mask
        self.num_input.setInputMask("999999999")
        input_font = self.num_input.font()
        input_font.setPointSize(24)
        self.num_input.setFont(input_font)

        quit_button = QPushButton('Quit')
        quit_button.clicked.connect(self.quit_function)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.submit_function)

        self.layout.addWidget(num_prompt, 0, 0, 1, 2)
        self.layout.addWidget(self.num_input, 1, 0, 1, 2)
        self.layout.addWidget(quit_button, 2, 0, 1, 1)
        self.layout.addWidget(submit_button, 2, 1, 1, 1)

        

        self.setWindowTitle("Provider Interface")
        self.resize(260, 150)

        self.createAlternateLayouts()

        self.setCurrentIndex(0)

        # self.show()

    def quit_function(self):
        self.hide()

    def submit_function(self):
        self.error_flag = False
        if self.db is None:
            deb.errp('Provider interface has no database.')
            return
        # Here we verify that the text entered is correct.
        entered = self.num_input.text().strip()
        self.input_test = self.db.getProvider(entered)
        if self.input_test is None:
            self.error_flag = True
        else:
            deb.debp('Provider successfully logged in.')
            # self.
            # self.setCurrentIndex(1)
            self.login()

    def verify_member(self):
        if self.db is None:
            deb.errp('Provider interface has no database.')
            return
        self.entered = self.verify_input.text().strip()
        deb.debp('Searching for member #' + self.entered)
        input_test = self.db.getMember(self.entered)
        if input_test is None:
            self.member_not_verified()
        else:
            if input_test.standing == 'Bad':
                self.member_not_verified()
            else:
                self.member_was_verified = True
                self.member_verified()
        self.edit4.setText(self.entered)
    
    def logout(self):
        self.setCurrentIndex(0)

    def login(self):
        self.setCurrentIndex(1)

    def verify(self):
        self.setCurrentIndex(2)
    
    def bill(self):
        self.billing = True
        self.edit5.setText(self.input_test.number)
        self.edit5.setReadOnly(True)
        self.edit4.setReadOnly(True)
        self.setCurrentIndex(2)

    def member_not_verified(self):
        self.setCurrentIndex(5)

    def member_verified(self):
        if self.billing == True:
            self.billing = False
            self.setCurrentIndex(6)
        else:
            self.setCurrentIndex(4)

    def update_billing(self):
        try:
            sinfo = self.pd.verify(int(self.codein.text().strip()))
        except ValueError:
            return
        if sinfo is not None:
            self.label7.setText(self.codein.text().strip() + ' - ' + str(sinfo[0]) + '. Fee: ' + str(sinfo[1]))
            self.can_bill = True

    def submit_billing(self):
        sdate = self.edit2.text().strip()
        mnum = self.edit4.text().strip()
        pnum = self.edit5.text().strip()
        snum = self.codein.text().strip()
        if sdate == '' or mnum == '' or pnum == '' or snum == '':
            return
        self.bc.verify(sdate, mnum, pnum, int(snum))
        self.login()

    def addDB(self, dbin):
        self.db = dbin
        self.bc = BillingController(dbin)

    def createAlternateLayouts(self):
        self.main_layout = QGridLayout()
        self.verify_layout = QGridLayout()
        self.bill_start = QGridLayout()

        main_label = QLabel('Provider Terminal Emulator V2.0')
        main_label.setFont(self.prompt_font)
        main_logout_b = QPushButton('Logout')
        main_verify_b = QPushButton('Verify')
        main_bill_b = QPushButton('Bill')

        main_logout_b.clicked.connect(self.logout)
        main_verify_b.clicked.connect(self.verify)
        main_bill_b.clicked.connect(self.bill)

        self.main_layout.addWidget(main_label, 0, 0, 1, 3)
        self.main_layout.addWidget(main_logout_b, 1, 0)
        self.main_layout.addWidget(main_verify_b, 1, 1)
        self.main_layout.addWidget(main_bill_b, 1, 2)

        verify_label = QLabel('Enter Member Number')
        prompt_font = verify_label.font()
        prompt_font.setPointSize(24)
        verify_label.setFont(prompt_font)

        self.verify_input = QLineEdit()
        self.verify_input.setInputMask("999999999")
        input_font = self.verify_input.font()
        input_font.setPointSize(24)
        self.verify_input.setFont(input_font)

        verify_back_b = QPushButton('Back')
        verify_back_b.clicked.connect(self.login)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.verify_member)

        self.verify_layout.addWidget(verify_label, 0, 0, 1, 2)
        self.verify_layout.addWidget(self.verify_input, 1, 0, 1, 2)
        self.verify_layout.addWidget(verify_back_b, 2, 0, 1, 1)
        self.verify_layout.addWidget(submit_button, 2, 1, 1, 1)

        self.login_ = QWidget()
        self.login_.setLayout(self.layout)
        self.addWidget(self.login_) # 0

        self.main_ = QWidget()
        self.verify_ = QWidget()
        self.bill_ = QWidget()
        self.main_.setLayout(self.main_layout)
        self.verify_.setLayout(self.verify_layout)
        self.bill_.setLayout(self.bill_start)
        self.addWidget(self.main_) # 1
        self.addWidget(self.verify_) # 2
        self.addWidget(self.bill_) # 3

        self.createIsVerifiedLayouts()
        self.createBillingLayouts()

    def createBillingLayouts(self):
        self.billing = QGridLayout()

        label1 = QLabel('Enter billing information')
        label2 = QLabel('Date of Service')
        # label3 = QLabel('Current Date')
        label4 = QLabel('Member Number')
        label5 = QLabel('Provider Number')
        label6 = QLabel('Service Code')

        self.edit2 = QLineEdit()
        # self.edit3 = QLineEdit()
        self.edit4 = QLineEdit()
        self.edit5 = QLineEdit()
        self.codein = QLineEdit()

        self.label7 = QLabel('Press Update to see service information.')

        button1 = QPushButton('Quit')
        button2 = QPushButton('Update')
        button3 = QPushButton('Submit')
        button1.clicked.connect(self.login)
        button2.clicked.connect(self.update_billing)
        button3.clicked.connect(self.submit_billing)

        # Add the widgets
        self.billing.addWidget(label1, 0, 0, 1, 2)
        self.billing.addWidget(label2, 1, 0)
        self.billing.addWidget(self.edit2, 1, 1, 1, 2)
        # self.billing.addWidget(label3, 2, 0)
        # self.billing.addWidget(self.edit3, 2, 1, 1, 2)
        self.billing.addWidget(label4, 3, 0)
        self.billing.addWidget(self.edit4, 3, 1, 1, 2)
        self.billing.addWidget(label5, 4, 0)
        self.billing.addWidget(self.edit5, 4, 1, 1, 2)
        self.billing.addWidget(label6, 5, 0)
        self.billing.addWidget(self.codein, 5, 1, 1, 2)
        self.billing.addWidget(self.label7, 6, 0, 1, 2)
        self.billing.addWidget(button1, 7, 0)
        self.billing.addWidget(button2, 7, 1)
        self.billing.addWidget(button3, 7, 2)

        # Create the widget
        self.billing_ = QWidget()
        # Set the layout
        self.billing_.setLayout(self.billing)
        # Add the widget
        self.addWidget(self.billing_) # 6

        

    def createIsVerifiedLayouts(self):
        self.verifiedl = QGridLayout()
        self.notverifiedl = QGridLayout()

        vlabel = QLabel('That is a verified member number.')
        nvlabel = QLabel('That member number could not be verified.')

        vbackb = QPushButton('Back')
        nvbackb = QPushButton('Back')

        vbackb.clicked.connect(self.login)
        nvbackb.clicked.connect(self.login)

        self.verifiedl.addWidget(vlabel, 0, 0, 1, 1)
        self.verifiedl.addWidget(vbackb, 1, 0, 1, 1)

        self.notverifiedl.addWidget(nvlabel, 0, 0)
        self.notverifiedl.addWidget(nvbackb, 1, 0)

        self.verified_ = QWidget()
        self.notverified_ = QWidget()

        self.verified_.setLayout(self.verifiedl)
        self.notverified_.setLayout(self.notverifiedl)
        
        self.addWidget(self.verified_) # 4
        self.addWidget(self.notverified_) # 5


class OperatorInterface(Interface):
    def setupUI(self):
        l = QLabel()
        self.prompt_font = l.font()
        self.prompt_font.setPointSize(22)

        self.gen_widgets()
        self.gen_layouts()
        self.set_widgets()

        self.setWindowTitle("Operator Interface")
        self.resize(300, 180)

        self.setCurrentIndex(0)

        # self.show()

    def gmain(self):
        """This goes to the main view."""
        self.setCurrentIndex(0)

    def delete_prov(self):
        self.db.removeProvider(self.num_input.text().strip())
        self.setCurrentIndex(0)

    def update_prov(self):
        self.db.editProvider(
            self.iname.text().strip(),
            self.istreet.text().strip(),
            self.icity.text().strip(),
            self.iprov.text().strip(),
            self.izip.text().strip(),
            self.iemail.text().strip(),
            self.num_input.text().strip()
        )
        self.setCurrentIndex(0)

    def delete_mem(self):
        # print(self.num_input.text().strip())
        self.db.removeMember(self.num_input.text().strip())
        self.setCurrentIndex(0)

    def update_mem(self):
        self.db.editMember(
            self.miname.text().strip(),
            self.mistreet.text().strip(),
            self.micity.text().strip(),
            self.miprov.text().strip(),
            self.mizip.text().strip(),
            self.miemail.text().strip(),
            self.num_input.text().strip()
        )
        self.setCurrentIndex(0)

    def quit(self):
        self.hide()

    def do_edit(self):
        if self.editing == 'PROVIDER':
            p = self.db.getProvider(self.num_input.text().strip())
            if p is not None:
                self.iname.setText(p.name)
                print(p.name + ' , ' + p.street)
                self.istreet.setText(p.street)
                self.icity.setText(p.city)
                self.iprov.setText(p.state)
                self.izip.setText(p.zip)
                self.iemail.setText(p.email)
            else:
                self.iname.setText('')
                self.istreet.setText('')
                self.icity.setText('')
                self.iprov.setText('')
                self.izip.setText('')
                self.iemail.setText('')
            self.setCurrentIndex(2)
        else:
            m = self.db.getMember(self.num_input.text().strip())
            if m is not None:
                self.miname.setText(m.name)
                self.mistreet.setText(m.street)
                self.micity.setText(m.city)
                self.miprov.setText(m.state)
                self.mizip.setText(m.zip)
                self.miemail.setText(m.email)
            else:
                self.miname.setText('')
                self.mistreet.setText('')
                self.micity.setText('')
                self.miprov.setText('')
                self.mizip.setText('')
                self.miemail.setText('')
            self.setCurrentIndex(3)

    def edit_p(self):
        self.editing = 'PROVIDER'
        self.setCurrentIndex(1)

    def edit_m(self):
        self.editing = 'MEMBER'
        self.setCurrentIndex(1)

    def gen_widgets(self):
        # These are the different 'scenes' of the application
        self.main_ = QWidget()
        self.prompt_ = QWidget()
        self.edit_p_ = QWidget()
        self.edit_m_ = QWidget()

    def set_widgets(self):
        self.main_.setLayout(self.mainl)
        self.addWidget(self.main_) # 0
        self.prompt_.setLayout(self.promptl)
        self.addWidget(self.prompt_) # 1
        self.edit_p_.setLayout(self.edit_pl)
        self.addWidget(self.edit_p_) # 2
        self.edit_m_.setLayout(self.edit_ml)
        self.addWidget(self.edit_m_) # 3

    def gen_layouts(self):
        self.mainl = QGridLayout()
        self.promptl = QGridLayout()
        self.edit_pl = QGridLayout()
        self.edit_ml = QGridLayout()

        self.gen_main()
        self.gen_prompt()
        self.gen_editp()
        self.gen_editm()

    def gen_main(self):
        label = QLabel('Welcome, Operator.')
        label.setFont(self.prompt_font)

        # Now we have buttons.

        quit_button = QPushButton('Quit')
        quit_button.clicked.connect(self.quit)
        editp_button = QPushButton('Edit Provider')
        editp_button.clicked.connect(self.edit_p)
        editm_button = QPushButton('Edit Member')
        editm_button.clicked.connect(self.edit_m)

        self.mainl.addWidget(label, 0, 0, 1, 3)
        self.mainl.addWidget(quit_button, 3, 0, 1, 1)
        self.mainl.addWidget(editm_button, 2, 1, 1, 2)
        self.mainl.addWidget(editp_button, 3, 1, 1, 2)

    def gen_prompt(self):
        num_prompt = QLabel('Enter Number') 
        num_prompt.setFont(self.prompt_font)

        self.num_input = QLineEdit()
        self.num_input.setInputMask("999999999")
        self.num_input.setFont(self.prompt_font)

        quit_button = QPushButton('Quit')
        quit_button.clicked.connect(self.quit)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.do_edit)

        self.promptl.addWidget(num_prompt, 0, 0, 1, 2)
        self.promptl.addWidget(self.num_input, 1, 0, 1, 2)
        self.promptl.addWidget(quit_button, 2, 0, 1, 1)
        self.promptl.addWidget(submit_button, 2, 1, 1, 1)

    def gen_editp(self):
        self.ep_prompt = QLabel('Enter Provider Information')
        label2 = QLabel('Name')
        label3 = QLabel('Street')
        label4 = QLabel('City')
        label5 = QLabel('Province')
        label6 = QLabel('Zip Code')
        label7 = QLabel('Email')

        self.iname = QLineEdit()
        self.istreet = QLineEdit()
        self.icity = QLineEdit()
        self.iprov = QLineEdit()
        self.izip = QLineEdit()
        self.iemail = QLineEdit()

        button1 = QPushButton('Quit')
        button2 = QPushButton('Delete')
        button3 = QPushButton('Submit')
        button1.clicked.connect(self.gmain)
        button2.clicked.connect(self.delete_prov)
        button3.clicked.connect(self.update_prov)

        # Add the widgets
        self.edit_pl.addWidget(self.ep_prompt, 0, 0, 1, 3)
        self.edit_pl.addWidget(label2, 1, 0)
        self.edit_pl.addWidget(self.iname, 1, 1, 1, 2)
        self.edit_pl.addWidget(label3, 2, 0)
        self.edit_pl.addWidget(self.istreet, 2, 1, 1, 2)
        self.edit_pl.addWidget(label4, 3, 0)
        self.edit_pl.addWidget(self.icity, 3, 1, 1, 2)
        self.edit_pl.addWidget(label5, 4, 0)
        self.edit_pl.addWidget(self.iprov, 4, 1, 1, 2)
        self.edit_pl.addWidget(label6, 5, 0)
        self.edit_pl.addWidget(self.izip, 5, 1, 1, 2)
        self.edit_pl.addWidget(label7, 6, 0)
        self.edit_pl.addWidget(self.iemail, 6, 1, 1, 2)
        self.edit_pl.addWidget(button1, 7, 0)
        self.edit_pl.addWidget(button2, 7, 1)
        self.edit_pl.addWidget(button3, 7, 2)

    def gen_editm(self):
        self.em_prompt = QLabel('Enter Member Information')
        label2 = QLabel('Name')
        label3 = QLabel('Street')
        label4 = QLabel('City')
        label5 = QLabel('Province')
        label6 = QLabel('Zip Code')
        label7 = QLabel('Email')

        self.miname = QLineEdit()
        self.mistreet = QLineEdit()
        self.micity = QLineEdit()
        self.miprov = QLineEdit()
        self.mizip = QLineEdit()
        self.miemail = QLineEdit()

        button1 = QPushButton('Quit')
        button2 = QPushButton('Delete')
        button3 = QPushButton('Submit')
        button1.clicked.connect(self.gmain)
        button2.clicked.connect(self.delete_mem)
        button3.clicked.connect(self.update_mem)

        # Add the widgets
        self.edit_ml.addWidget(self.em_prompt, 0, 0, 1, 3)
        self.edit_ml.addWidget(label2, 1, 0)
        self.edit_ml.addWidget(self.miname, 1, 1, 1, 2)
        self.edit_ml.addWidget(label3, 2, 0)
        self.edit_ml.addWidget(self.mistreet, 2, 1, 1, 2)
        self.edit_ml.addWidget(label4, 3, 0)
        self.edit_ml.addWidget(self.micity, 3, 1, 1, 2)
        self.edit_ml.addWidget(label5, 4, 0)
        self.edit_ml.addWidget(self.miprov, 4, 1, 1, 2)
        self.edit_ml.addWidget(label6, 5, 0)
        self.edit_ml.addWidget(self.mizip, 5, 1, 1, 2)
        self.edit_ml.addWidget(label7, 6, 0)
        self.edit_ml.addWidget(self.miemail, 6, 1, 1, 2)
        self.edit_ml.addWidget(button1, 7, 0)
        self.edit_ml.addWidget(button2, 7, 1)
        self.edit_ml.addWidget(button3, 7, 2)

    def addDB(self, dbin):
        self.db = dbin
        

class ManagerInterface(Interface):
    def setupUI(self):
        
        self.gen_UI()
        self.rg = ReportGeneration()
	
        self.setWindowTitle("Manager Simulation")
        self.resize(260, 150)
        self.setCurrentIndex(0)

    def preport(self):
        p = self.db.getProvider(self.pedit.text().strip())
        if p is None:
            self.statusl.setText('That Provider number is invalid!')
            return
        self.rg.printProviderReport(p)
        self.statusl.setText('Provider report generated.')

    def mreport(self):
        m = self.db.getMember(self.medit.text().strip())
        if m is None:
            self.statusl.setText('That Member number is invalid!')
            return
        print(m.name)
        self.rg.printMemberReport(m)
        self.statusl.setText('Member report generated.')

    def sreport(self):
        if not self.db.providers:
            self.statusl.setText('There are no providers.')
            return
        self.rg.printSummaryReport(self.db.providers)
        self.statusl.setText('Summary report generated.')

    def addDB(self, dbin):
        self.db = dbin

    def gen_UI(self):
        main = QLabel('Generate Reports')
        self.statusl = QLabel('')
        labelp = QLabel('Provider Number')
        labelm = QLabel('Member Number')

        self.pedit = QLineEdit()
        self.medit = QLineEdit()

        pbut = QPushButton('Generate Report')
        pbut.clicked.connect(self.preport)
        mbut = QPushButton('Generate Report')
        mbut.clicked.connect(self.mreport)
        sbut = QPushButton('Generate Summary Report')
        sbut.clicked.connect(self.sreport)

        # Now we create the layout to hold these.

        self.layout = QGridLayout()

        self.layout.addWidget(main, 0, 0, 1, 2)    
        self.layout.addWidget(self.statusl, 1, 0, 1, 2)    
        self.layout.addWidget(labelp, 2, 0)    
        self.layout.addWidget(labelm, 2, 1)    
        self.layout.addWidget(self.pedit, 3, 0)    
        self.layout.addWidget(self.medit, 3, 1)    
        self.layout.addWidget(pbut, 4, 0)    
        self.layout.addWidget(mbut, 4, 1)    
        self.layout.addWidget(sbut, 5, 0, 1, 2)    

        self.main_ = QWidget()
        self.main_.setLayout(self.layout)
        self.addWidget(self.main_)

def test_interface():
    a = QApplication(sys.argv)
    p = ProviderInterface(None)
    sys.exit(a.exec_())

if __name__ == '__main__':
    test_interface()
