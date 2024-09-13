import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 280, 150)

        # Crear los widgets
        self.username_label = QLabel('Username:', self)
        self.username_input = QLineEdit(self)
        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Login', self)
        self.logout_button = QPushButton('Logout', self)

        # Crear layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.logout_button)

        # Crear un contenedor y asignarle el layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Conectar los botones a las funciones
        self.login_button.clicked.connect(self.login)
        self.logout_button.clicked.connect(self.logout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Hacer petición al servidor local
        try:
            response = requests.post('http://127.0.0.1:5000/login', json={'username': username, 'password': password})

            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Login successful!')
                # Aquí puedes cerrar la ventana de login y abrir la ventana principal
                self.open_admin_window()
            else:
                QMessageBox.warning(self, 'Error', 'Login failed.')
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'Could not connect to the server: {e}')

    def logout(self):
        try:
            response = requests.post('http://127.0.0.1:5000/logout')

            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Logout successful!')
            else:
                QMessageBox.warning(self, 'Error', 'Logout failed.')
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'Could not connect to the server: {e}')

    def open_admin_window(self):
        self.hide()
        self.admin_window = AdminWindow()
        self.admin_window.show()


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin User Management')
        self.setGeometry(100, 100, 400, 300)

        # Aquí puedes agregar los elementos y funciones de la administración de usuarios
        # como obtener la lista de usuarios, agregar o eliminar usuarios


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
