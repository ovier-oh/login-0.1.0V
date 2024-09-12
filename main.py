import sys 
import requests 
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox 

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

        # Creando layout
        layout = QVBoxLayout() 
        layout = addWidget(self.username_label)
        layout = addWidget(self.username_input) 
        layout = addWidget(self.password_label)
        layout = addWidget(self.password_input) 
        layout = addWidget(self.login_button)
        layout = addWidget(self.logout_button) 
        