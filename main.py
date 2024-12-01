import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet
from database import engine, SessionLocal
import models
from ui.login import LoginWidget
from ui.register import RegisterWidget
from ui.main_window import MainWindow

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления пассажирами")
        self.setGeometry(100, 100, 1200, 800)

        # Создаем базу данных
        models.Base.metadata.create_all(bind=engine)

        # Инициализируем центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Создаем стек виджетов
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # Создаем виджеты для разных экранов
        self.login_widget = LoginWidget(self)
        self.register_widget = RegisterWidget(self)
        self.main_window = MainWindow(self)

        # Добавляем виджеты в стек
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.register_widget)
        self.stack.addWidget(self.main_window)

        # Начинаем с экрана входа
        self.stack.setCurrentWidget(self.login_widget)

    def show_login(self):
        self.stack.setCurrentWidget(self.login_widget)

    def show_register(self):
        self.stack.setCurrentWidget(self.register_widget)

    def show_main(self):
        self.stack.setCurrentWidget(self.main_window)

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    def show_success(self, message):
        QMessageBox.information(self, "Успех", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_teal.xml')
    window = App()
    window.show()
    sys.exit(app.exec())
