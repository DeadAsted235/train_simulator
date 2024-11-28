from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                           QPushButton, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from database import SessionLocal
import auth

class RegisterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Добавляем растягивающийся элемент сверху
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Создаем центральный виджет с фиксированной шириной
        center_widget = QWidget()
        center_widget.setFixedWidth(400)
        layout = QGridLayout()
        center_widget.setLayout(layout)

        # Заголовок
        title = QLabel("Регистрация")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            margin: 20px;
            color: #1976D2;
            font-weight: bold;
        """)
        layout.addWidget(title, 0, 0, 1, 2)

        # Стили для полей ввода
        input_style = """
            QLineEdit {
                padding: 8px;
                border: 2px solid #BDBDBD;
                border-radius: 4px;
                margin: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #1976D2;
            }
        """

        # Поля ввода
        username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя пользователя")
        self.username_input.setStyleSheet(input_style)

        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Введите email")
        self.email_input.setStyleSheet(input_style)
        
        password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)

        confirm_password_label = QLabel("Подтвердите пароль:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setStyleSheet(input_style)

        # Стили для меток
        label_style = """
            QLabel {
                color: #424242;
                font-weight: bold;
            }
        """
        for label in [username_label, email_label, password_label, confirm_password_label]:
            label.setStyleSheet(label_style)

        layout.addWidget(username_label, 1, 0)
        layout.addWidget(self.username_input, 1, 1)
        layout.addWidget(email_label, 2, 0)
        layout.addWidget(self.email_input, 2, 1)
        layout.addWidget(password_label, 3, 0)
        layout.addWidget(self.password_input, 3, 1)
        layout.addWidget(confirm_password_label, 4, 0)
        layout.addWidget(self.confirm_password_input, 4, 1)

        # Кнопки
        register_btn = QPushButton("Зарегистрироваться")
        register_btn.clicked.connect(self.register)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                min-width: 150px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #43A047;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        
        back_btn = QPushButton("Назад")
        back_btn.clicked.connect(self.parent.show_login)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                min-width: 100px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        """)

        layout.addWidget(register_btn, 5, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_btn, 6, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Добавляем центральный виджет в основной layout
        main_layout.addWidget(center_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Добавляем растягивающийся элемент снизу
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not all([username, email, password, confirm_password]):
            self.parent.show_error("Пожалуйста, заполните все поля")
            return

        if password != confirm_password:
            self.parent.show_error("Пароли не совпадают")
            return

        with SessionLocal() as db:
            try:
                auth.create_user(db, username, email, password)
                self.parent.show_success("Регистрация успешна")
                self.parent.show_login()
            except Exception as e:
                self.parent.show_error(f"Ошибка при регистрации: {str(e)}")
