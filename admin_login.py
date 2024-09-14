import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                             QWidget, QMessageBox, QHBoxLayout, QFrame, QDesktopWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from admin_gui import AdminWindow  # Importa el dashboard de administración de usuarios


class AdminLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login de Administrador')
        self.setGeometry(100, 100, 800, 400)  # Ajustar el tamaño de la ventana

        # Centrar la ventana
        self.center_window()

        # Crear el diseño principal (dividido en dos secciones)
        main_layout = QHBoxLayout()

        # Sección de la izquierda (Formulario de Login)
        login_frame = QFrame()
        login_frame.setStyleSheet("background-color: white;")
        login_layout = QVBoxLayout()

        # Centrar el contenido del login
        login_layout.setAlignment(Qt.AlignCenter)

        # Título "Login"
        login_title = QLabel("Login")
        login_title.setFont(QFont('Arial', 24, QFont.Bold))
        login_title.setAlignment(Qt.AlignCenter)
        login_title.setStyleSheet("color: black;")

        # Campo de Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        self.username_input.setFixedWidth(300)  # Ancho fijo
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding-left: 30px;
                border: 2px solid gray;
                border-radius: 20px;
                font-size: 14px;
            }
        """)

        # Campo de Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setFixedWidth(300)  # Ancho fijo
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding-left: 30px;
                border: 2px solid gray;
                border-radius: 20px;
                font-size: 14px;
            }
        """)

        # Botón de Login
        login_button = QPushButton("Login")
        login_button.setFixedHeight(40)
        login_button.setFixedWidth(300)  # Ancho fijo
        login_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: gray;
            }
        """)

        # Texto "Don't have an account? Sign Up"
        signup_label = QLabel("Don't have an account? <a href='#'>Sign Up</a>")
        signup_label.setAlignment(Qt.AlignCenter)
        signup_label.setStyleSheet("color: gray; font-size: 12px;")
        signup_label.setOpenExternalLinks(True)

        # Añadir los widgets al layout del formulario
        login_layout.addWidget(login_title)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(login_button)
        login_layout.addWidget(signup_label)

        # Asignar layout al frame de login
        login_frame.setLayout(login_layout)

        # Sección de la derecha (Bienvenida)
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet("background-color: black; color: white;")
        welcome_layout = QVBoxLayout()

        # Centrar el contenido de la bienvenida
        welcome_layout.setAlignment(Qt.AlignCenter)

        welcome_title = QLabel("WELCOME\nADMIN!")
        welcome_title.setFont(QFont('Arial', 24, QFont.Bold))
        welcome_title.setAlignment(Qt.AlignCenter)

        welcome_text = QLabel("Gestión de usuarios y configuraciones\nespeciales para administradores.")
        welcome_text.setFont(QFont('Arial', 12))
        welcome_text.setAlignment(Qt.AlignCenter)

        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_text)

        welcome_frame.setLayout(welcome_layout)

        # Añadir las dos secciones al layout principal
        main_layout.addWidget(login_frame, 1)  # Ocupa el 50% del espacio
        main_layout.addWidget(welcome_frame, 1)  # Ocupa el otro 50%

        # Crear un widget para el layout principal
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

        # Conectar el botón de login a la función
        login_button.clicked.connect(self.login)

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
