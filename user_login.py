import sys
import requests
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, 
                             QWidget, QMessageBox, QHBoxLayout, QLineEdit, QFrame, QDesktopWidget)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class UserLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login de Usuario')
        self.setGeometry(100, 100, 800, 400)  # Ajustar el tamaño de la ventana

        # Centrar la ventana en la pantalla
        self.center_window()

        # Crear el diseño principal (dividido en dos secciones)
        main_layout = QHBoxLayout()

        # Sección de la izquierda (Formulario de Login)
        login_frame = QFrame()
        login_frame.setStyleSheet("background-color: white;")
        login_layout = QVBoxLayout()

        # Título "Login"
        login_title = QLabel("Login")
        login_title.setFont(QFont('Arial', 24, QFont.Bold))
        login_title.setAlignment(Qt.AlignCenter)
        login_title.setStyleSheet("color: black;")

        # Campo de Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
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

        welcome_title = QLabel("WELCOME\nBACK!")
        welcome_title.setFont(QFont('Arial', 24, QFont.Bold))
        welcome_title.setAlignment(Qt.AlignCenter)

        welcome_text = QLabel("Lorem ipsum dolor sit amet consectetur\nadipiscing elit. Delentir?")
        welcome_text.setFont(QFont('Arial', 12))
        welcome_text.setAlignment(Qt.AlignCenter)

        welcome_layout.addStretch(1)  # Añadir un espacio
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_text)
        welcome_layout.addStretch(1)  # Añadir un espacio

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

        # Hacer petición al servidor local para el usuario regular
        try:
            response = requests.post('http://127.0.0.1:5000/login', json={'username': username, 'password': password})

            if response.status_code == 200 and username != "Admin":
                QMessageBox.information(self, 'Success', 'Login successful!')
                # Aquí puedes cerrar la ventana de login y abrir el dashboard del usuario
                self.open_user_dashboard()
            else:
                QMessageBox.warning(self, 'Error', 'Login failed or Admin account used.')
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'Could not connect to the server: {e}')

    def open_user_dashboard(self):
        """Cierra la ventana de login y abre el dashboard de usuario"""
        self.hide()
        self.user_dashboard = UserDashboardWindow()  # Abre el dashboard con 5 botones
        self.user_dashboard.show()


class UserDashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Aumentamos el tamaño de la ventana
        self.setWindowTitle('Dashboard de Usuario')
        self.setGeometry(100, 100, 1000, 600)  # Tamaño aumentado a 1000x600

        # Centrar la ventana en la pantalla
        self.center_window()

        # Crear un QLabel grande con el texto "Simulador SDSSP"
        title_label = QLabel("Simulador \nSDSSP", self)
        title_font = QFont("Arial", 24, QFont.Bold)  # Ajustar el tamaño y la fuente
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)  # Centrar el texto

        # Ruta a la carpeta de imágenes
        img_path = os.path.join(os.getcwd(), 'img')

        # Crear las imágenes y los botones del dashboard
        self.resistor_layout = self.create_image_with_button('Resistor', os.path.join(img_path, 'resistor.webp'))
        self.capacitor_layout = self.create_image_with_button('Condensador', os.path.join(img_path, 'capacitor.webp'))
        self.transistor_layout = self.create_image_with_button('Transistor', os.path.join(img_path, 'diode.webp'))
        self.diode_layout = self.create_image_with_button('Diodo', os.path.join(img_path, 'bjt.webp'))
        self.inductor_layout = self.create_image_with_button('Inductor', os.path.join(img_path, 'mosfet.webp'))

        # Layout horizontal para las imágenes y botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addLayout(self.resistor_layout)
        buttons_layout.addLayout(self.capacitor_layout)
        buttons_layout.addLayout(self.transistor_layout)
        buttons_layout.addLayout(self.diode_layout)
        buttons_layout.addLayout(self.inductor_layout)

        # Centrar el layout de botones
        buttons_layout.setAlignment(Qt.AlignCenter)

        # Layout vertical principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)  # Añadir el título grande arriba
        main_layout.addLayout(buttons_layout)  # Añadir el layout de botones

        # Contenedor
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_image_with_button(self, label_text, image_path):
        """Crea un layout con una imagen arriba y un botón debajo"""
        layout = QVBoxLayout()

        # Imagen del componente escalada x3
        pixmap = QPixmap(image_path)
        image_label = QLabel()
        image_label.setPixmap(pixmap.scaled(150, 150))  # Escalar la imagen por un factor de 3 (150x150)

        # Botón con el texto del componente (centrado)
        button = QPushButton(label_text)
        button.setFixedWidth(150)  # Ajustar el ancho del botón al tamaño de la imagen
        button.clicked.connect(lambda: self.show_message(label_text))

        # Añadir la imagen y el botón al layout y centrar
        layout.addWidget(image_label)
        layout.addWidget(button)
        layout.setAlignment(Qt.AlignCenter)  # Centrar cada imagen y botón

        return layout

    def show_message(self, label_text):
        QMessageBox.information(self, label_text, f'Has presionado el botón para {label_text}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = UserLoginWindow()
    login_window.show()
    sys.exit(app.exec_())