from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                           QPushButton, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from database import SessionLocal
import auth

class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Основной контейнер
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Добавляем растягивающийся элемент сверху
        main_layout.addStretch(1)

        # Создаем центральный виджет с фиксированной шириной
        center_widget = QWidget()
        center_widget.setFixedWidth(400)
        layout = QGridLayout()
        center_widget.setLayout(layout)

        # Заголовок
        title = QLabel("Вход в систему")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            margin: 20px;
            color: #1976D2;
            font-weight: bold;
            padding: 20px;
        """)
        layout.addWidget(title, 0, 0, 1, 2)

        # Стили для полей ввода
        input_style = """
            QLineEdit {
                padding: 12px;
                border: 2px solid #BDBDBD;
                border-radius: 6px;
                margin: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #1976D2;
            }
        """

        # Стили для меток
        label_style = """
            QLabel {
                font-size: 14px;
                color: #424242;
                font-weight: bold;
                margin: 8px;
            }
        """

        # Поля ввода
        username_label = QLabel("Имя пользователя:")
        username_label.setStyleSheet(label_style)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя пользователя")
        self.username_input.setStyleSheet(input_style)
        
        password_label = QLabel("Пароль:")
        password_label.setStyleSheet(label_style)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)

        # Добавляем поля в сетку
        layout.addWidget(username_label, 1, 0)
        layout.addWidget(self.username_input, 1, 1)
        layout.addWidget(password_label, 2, 0)
        layout.addWidget(self.password_input, 2, 1)

        # Кнопки
        button_style = """
            QPushButton {
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
                margin: 10px;
            }
        """

        login_btn = QPushButton("Войти")
        login_btn.clicked.connect(self.login)
        login_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #1976D2;
                color: white;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        
        register_btn = QPushButton("Регистрация")
        register_btn.clicked.connect(self.parent.show_register)
        register_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #43A047;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)

        # Добавляем кнопки в сетку
        button_container = QWidget()
        button_layout = QVBoxLayout()
        button_container.setLayout(button_layout)
        button_layout.addWidget(login_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(register_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button_container, 3, 0, 1, 2)

        # Добавляем центральный виджет в основной layout
        main_layout.addWidget(center_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Добавляем растягивающийся элемент снизу
        main_layout.addStretch(1)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.parent.show_error("Пожалуйста, заполните все поля")
            return

        with SessionLocal() as db:
            user = auth.authenticate_user(db, username, password)
            if user:
                self.parent.user = user
                self.parent.show_main()
            else:
                self.parent.show_error("Неверное имя пользователя или пароль")
