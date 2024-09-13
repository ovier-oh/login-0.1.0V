import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from admin_gui import AdminWindow  # Importa el dashboard de administración de usuarios


class AdminLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login de Administrador')
        self.setGeometry(100, 100, 280, 150)

        # Crear los widgets
        self.username_label = QLabel('Username:', self)
        self.username_input = QLineEdit(self)
        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Login', self)

        # Crear layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        # Crear un contenedor y asignarle el layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Conectar el botón de login a la función
        self.login_button.clicked.connect(self.login)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Verificar si el usuario y la contraseña están en el archivo admins.txt
        if self.check_admin_credentials(username, password):
            QMessageBox.information(self, 'Success', 'Login successful!')
            self.open_admin_dashboard()
        else:
            QMessageBox.warning(self, 'Error', 'Login failed. Invalid credentials.')

    def check_admin_credentials(self, username, password):
        """Verifica las credenciales del archivo admins.txt"""
        try:
            with open('admins.txt', 'r') as file:
                for line in file:
                    admin_user, admin_pass = line.strip().split(',')
                    if admin_user == username and admin_pass == password:
                        return True
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'Archivo admins.txt no encontrado.')
        return False

    def open_admin_dashboard(self):
        """Cierra la ventana de login y abre el dashboard de administración de usuarios"""
        self.hide()
        self.admin_window = AdminWindow()  # Usa el AdminWindow importado
        self.admin_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = AdminLoginWindow()
    login_window.show()
    sys.exit(app.exec_())
