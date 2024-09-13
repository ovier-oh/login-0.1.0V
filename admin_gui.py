import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QHBoxLayout, QMessageBox
import requests


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Admin User Management')
        self.setGeometry(100, 100, 600, 400)

        # Crear los widgets
        self.table_widget = QTableWidget()
        self.load_users_button = QPushButton('Cargar usuarios')
        self.add_user_button = QPushButton('Añadir nuevo usuario')

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.load_users_button)
        layout.addWidget(self.add_user_button)
        layout.addWidget(self.table_widget)

        # Crear un contenedor
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Conectar botones a funciones
        self.load_users_button.clicked.connect(self.load_users)
        self.add_user_button.clicked.connect(self.show_add_user_form)

    def load_users(self):
        """Carga la lista de usuarios desde el servidor"""
        try:
            response = requests.get('http://127.0.0.1:5000/users')
            if response.status_code == 200:
                users = response.json()
                self.populate_table(users)
            else:
                QMessageBox.warning(self, 'Error', 'Error al cargar usuarios')
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'Error de conexión: {e}')

    def populate_table(self, users):
        """Llena la tabla con la lista de usuarios"""
        self.table_widget.setRowCount(len(users))
        self.table_widget.setColumnCount(6)  # Añadimos una columna para el botón de eliminar
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Nombre', 'Edad', 'Teléfono', 'Correo', 'Acciones'])

        for i, user in enumerate(users):
            for j, value in enumerate(user):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(value)))

            # Crear el botón de eliminar
            delete_button = QPushButton('Eliminar')
            delete_button.clicked.connect(lambda _, row=user[0]: self.delete_user(row))
            self.table_widget.setCellWidget(i, 5, delete_button)

    def delete_user(self, user_id):
        """Elimina un usuario enviando una solicitud al servidor"""
        confirmation = QMessageBox.question(self, 'Confirmación', f'¿Seguro que deseas eliminar al usuario con ID {user_id}?', 
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation == QMessageBox.Yes:
            try:
                response = requests.delete(f'http://127.0.0.1:5000/delete_user/{user_id}')
                if response.status_code == 200:
                    QMessageBox.information(self, 'Éxito', 'Usuario eliminado correctamente')
                    self.load_users()  # Recargar la lista de usuarios después de eliminar
                else:
                    QMessageBox.warning(self, 'Error', 'No se pudo eliminar el usuario')
            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, 'Error', f'Error de conexión: {e}')

    def show_add_user_form(self):
        """Muestra un formulario para agregar un nuevo usuario"""
        self.add_user_form = AddUserForm()
        self.add_user_form.show()


class AddUserForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Añadir nuevo usuario')
        self.setGeometry(200, 200, 400, 300)

        # Crear los campos
        self.name_label = QLabel('Nombre:')
        self.name_input = QLineEdit(self)
        self.age_label = QLabel('Edad:')
        self.age_input = QLineEdit(self)
        self.phone_label = QLabel('Teléfono:')
        self.phone_input = QLineEdit(self)
        self.email_label = QLabel('Correo electrónico:')
        self.email_input = QLineEdit(self)
        self.username_label = QLabel('Nombre de usuario:')
        self.username_input = QLineEdit(self)
        self.password_label = QLabel('Contraseña:')
        self.password_input = QLineEdit(self)

        # Botón de agregar
        self.add_button = QPushButton('Agregar Usuario')

        # Layout del formulario
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.age_label)
        form_layout.addWidget(self.age_input)
        form_layout.addWidget(self.phone_label)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(self.email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.add_button)

        self.setLayout(form_layout)

        # Conectar el botón de agregar usuario
        self.add_button.clicked.connect(self.add_user)

    def add_user(self):
        """Agrega un nuevo usuario al servidor"""
        user_data = {
            'nombre': self.name_input.text(),
            'edad': self.age_input.text(),
            'telefono': self.phone_input.text(),
            'email': self.email_input.text(),
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }

        try:
            response = requests.post('http://127.0.0.1:5000/add_user', json=user_data)
            if response.status_code == 201:
                QMessageBox.information(self, 'Éxito', 'Usuario agregado correctamente')
                self.close()  # Cierra el formulario al agregar el usuario
            else:
                QMessageBox.warning(self, 'Error', 'No se pudo agregar el usuario')
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'Error de conexión: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_window = AdminWindow()
    admin_window.show()
    sys.exit(app.exec_())
