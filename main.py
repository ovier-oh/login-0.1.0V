import sys 
import requests 
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QBoxLayout, QWidget, QMessageBox 

class LoginWindow(QMainWindow):
    def __init_(self):
        super().__init__() 

        self.setWindowTitle('Login')
        self.setGeometry(100,100, 200, 150) 

        #Crear los widgets 
        self.username_label = QLabel('Username:',self)
        self.username_input = QLineEdit(self) 
        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Login', self) 
        self.logout_button = QPushButton('Logout', self) 

        