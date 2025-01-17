from src_.main_window_ui import *



from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressBar, QLabel, QCheckBox, QSpinBox, QLineEdit, QWidget
from PyQt5.uic import loadUi

from os import path
from subprocess import check_output, DEVNULL
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from firebase_admin import credentials, initialize_app, storage, db, delete_app

import os
import sys
from datetime import datetime, timedelta
from fake_useragent import UserAgent

from CoreSecurity.keys.keys import *
from CoreSecurity.Security import *
from CoreApp.QProcess.RotateVpnThread.Qt5 import RotateVpnThread
from CoreApp.QProcess.BenchmarkWindow import BenchmarkWindow
from CoreApp.QProcess.GlobalBenchmarkWindow import GlobalBenchmarkWindow

diretorio_script = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(diretorio_script, 'CoreApp', 'config', 'user_config.json')
BENCHMARK_FILE = os.path.join(diretorio_script, 'CoreApp', 'config', 'benchmark_data.json')

class Main_Window_Auto_Rotate(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Nord Vpn Auto Rotate')
        logo_FILE = os.path.join(diretorio_script, 'src_', 'icons', 'logo2.png')
        style_FILE = os.path.join(diretorio_script, 'src_', 'style.qss')
        self.setWindowIcon(QIcon(logo_FILE))
        with open(style_FILE, 'r') as f:
            self.setStyleSheet(f.read())
        self.logoLabel = self.ui.logoLabel
        self.logoLabel.setPixmap(QPixmap(logo_FILE).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.rotateButton = self.ui.rotateButton
        self.rotateButton.clicked.connect(self.on_rotate_button_clicked)
        self.stopButton = self.ui.stopButton
        self.stopButton.clicked.connect(self.on_stop_button_clicked)
        self.progressBar = self.ui.progressBar
        self.locationLabel = self.ui.locationLabel
        self.usaCheckBox = self.ui.usaCheckBox 
        self.canadacheckBox = self.ui.canadacheckBox
        self.completecheckBox = self.ui.completecheckBox
        self.lineEdit = self.ui.lineEdit
        self.rotationCountSpinBox = self.ui.rotationCountSpinBox
        self.intervalSpinBox = self.ui.intervalSpinBox
        self.benchmarkButton = self.ui.benchmarkButton
        self.benchmarkButton.clicked.connect(self.on_benchmark_button_clicked)
        self.globalBenchmarkButton = self.ui.globalBenchmarkButton
        self.globalBenchmarkButton.clicked.connect(self.on_global_benchmark_button_clicked)
        self.usaCheckBox.stateChanged.connect(self.update_checkboxes)
        self.canadacheckBox.stateChanged.connect(self.update_checkboxes)
        self.completecheckBox.stateChanged.connect(self.update_checkboxes)

        self.load_config()

    def update_checkboxes(self):
        flagcanadacheckBox = self.canadacheckBox.isChecked()
        flagusaCheckBox = self.usaCheckBox.isChecked()
        flagcompletecheckBox= self.completecheckBox.isChecked()

        if flagcanadacheckBox == True:
            
            self.usaCheckBox.setChecked(False)
            self.completecheckBox.setChecked(False)

        if flagusaCheckBox == True:
            self.canadacheckBox.setChecked(False)
            self.completecheckBox.setChecked(False)

        if flagcompletecheckBox == True:
            self.canadacheckBox.setChecked(False)
            self.usaCheckBox.setChecked(False)

    def on_rotate_button_clicked(self):
        rotation_count = self.rotationCountSpinBox.value()
        interval = self.intervalSpinBox.value()
        rotate_in_usa = self.usaCheckBox.isChecked()
        rotate_in_canada = self.canadacheckBox.isChecked()
        rotate_in_complete = self.completecheckBox.isChecked()
        nvar_key = self.lineEdit.text()

        self.Rotate_Vpn_Thread = RotateVpnThread(rotation_count, interval, rotate_in_usa, rotate_in_canada, rotate_in_complete, nvar_key)
        self.Rotate_Vpn_Thread.progress.connect(self.update_progress)
        self.Rotate_Vpn_Thread.location.connect(self.update_location)
        self.Rotate_Vpn_Thread.finished.connect(self.on_rotation_finished)
        self.Rotate_Vpn_Thread.start()

    def on_stop_button_clicked(self):
        if hasattr(self, 'Rotate_Vpn_Thread') and self.Rotate_Vpn_Thread.isRunning():
            self.Rotate_Vpn_Thread.stop()
            self.Rotate_Vpn_Thread.wait()
            self.on_rotation_finished()

    def on_benchmark_button_clicked(self):
        self.benchmarkWindow = BenchmarkWindow()
        self.benchmarkWindow.show()

    def on_global_benchmark_button_clicked(self):
        globalBenchmarkWindow = GlobalBenchmarkWindow()
        globalBenchmarkWindow.show()

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def update_location(self, location):
        self.locationLabel.setText(location)

    def on_rotation_finished(self):
        self.rotateButton.setEnabled(True)
        self.stopButton.setEnabled(False)

    # def resizeEvent(self, event):
    #     if self.width() > self.height():
    #         print('Landscape Mode')
    #     else:
    #         print('Portrait Mode')
    #     super(MainWindow, self).resizeEvent(event)

    def closeEvent(self, event):
        self.save_config()
        event.accept()


    def load_config(self):
        try:
            security = Security(app1=app1)
            respostaname_machine = security.get_machine_info()
            ref1 = db.reference(f'save_settings_users/{respostaname_machine}', app=app1)
            data1 = ref1.get()                         
            rotation_count = data1["rotation_count"]
            interval = data1["interval"]
            rotate_in_usa = data1["rotate_in_usa"]
            rotate_in_canada = data1["rotate_in_canada"]
            key_save = data1["key_save"]
            rotate_complete = data1["rotate_complete"]

            def str_to_bool(s):
                return s.lower() in ['true', '1', 't', 'y', 'yes']

            self.rotationCountSpinBox.setValue(int(rotation_count))
            self.intervalSpinBox.setValue(int(interval))
            self.usaCheckBox.setChecked(str_to_bool(rotate_in_usa))
            self.canadacheckBox.setChecked(str_to_bool(rotate_in_canada))
            self.completecheckBox.setChecked(str_to_bool(rotate_complete))
            self.lineEdit.setText(str(key_save))
        except Exception as e:
            security = Security(app1=app1)
            respostaname_machine = security.get_machine_info()
            ref1 = db.reference(f'save_settings_users', app=app1)
            data1 = ref1.get()                         
            controle_das_funcao2 = f"{respostaname_machine}"
            controle_das_funcao_info_2 = {
            "rotation_count": f"{self.rotationCountSpinBox.value()}",
            "interval": f"{self.intervalSpinBox.value()}",
            "rotate_in_usa": f"{self.usaCheckBox.isChecked()}",
            "rotate_in_canada": f"{self.canadacheckBox.isChecked()}",
            "key_save": f"{self.lineEdit.text()}",
            "rotate_complete": f"{self.completecheckBox.isChecked()}",
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

    def save_config(self):
        security = Security(app1=app1)
        respostaname_machine = security.get_machine_info()
        ref1 = db.reference(f'save_settings_users', app=app1)
        data1 = ref1.get()                         
        controle_das_funcao2 = f"{respostaname_machine}"
        controle_das_funcao_info_2 = {
        "rotation_count": f"{self.rotationCountSpinBox.value()}",
        "interval": f"{self.intervalSpinBox.value()}",
        "rotate_in_usa": f"{self.usaCheckBox.isChecked()}",
        "rotate_in_canada": f"{self.canadacheckBox.isChecked()}",
        "key_save": f"{self.lineEdit.text()}",
        "rotate_complete": f"{self.completecheckBox.isChecked()}",
        }
        ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Main_Window_Auto_Rotate()
    MainWindow.show()
    sys.exit(app.exec())