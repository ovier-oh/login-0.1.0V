import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap, QFont
import os
from PyQt5.QtCore import Qt


class UserLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login de Usuario')
        self.setGeometry(100, 100, 280, 150)

        # Crear los widgets de login
        self.username_label = QLabel('Username:', self)
        self.username_input = QLineEdit(self)
        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Login', self)

        # Crear layout de login
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
