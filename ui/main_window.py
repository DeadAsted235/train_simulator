from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QLineEdit,
                             QDateTimeEdit, QMessageBox, QHBoxLayout, QHeaderView,
                             QDialogButtonBox)
from PyQt6.QtCore import Qt, QDateTime
from database import SessionLocal
from models import Passenger, Train, Ticket
import openpyxl
from datetime import datetime


class PassengerDialog(QDialog):
    def __init__(self, parent=None, passenger=None):
        super().__init__(parent)
        self.passenger = passenger
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Добавить пассажира" if not self.passenger else "Редактировать пассажира")
        self.setFixedWidth(500)
        layout = QFormLayout()
        self.setLayout(layout)

        # Стили для полей ввода
        input_style = """
            QLineEdit, QDateTimeEdit {
                padding: 8px;
                border: 2px solid #BDBDBD;
                border-radius: 4px;
                margin: 5px;
            }
            QLineEdit:focus, QDateTimeEdit:focus {
                border: 2px solid #1976D2;
            }
        """

        # Создаем поля ввода
        self.first_name = QLineEdit(self.passenger.first_name if self.passenger else "")
        self.last_name = QLineEdit(self.passenger.last_name if self.passenger else "")
        self.middle_name = QLineEdit(self.passenger.middle_name if self.passenger else "")
        self.passport = QLineEdit(self.passenger.passport_number if self.passenger else "")
        self.train_name = QLineEdit(self.passenger.train_name if self.passenger else "")
        self.departure_station = QLineEdit(self.passenger.departure_station if self.passenger else "")
        self.arrival_station = QLineEdit(self.passenger.arrival_station if self.passenger else "")
        self.seat_number = QLineEdit(self.passenger.seat_number if self.passenger else "")

        self.departure_time = QDateTimeEdit()
        self.arrival_time = QDateTimeEdit()

        # Применяем стили
        for widget in [self.first_name, self.last_name, self.middle_name, self.passport, self.train_name,
                       self.departure_station, self.arrival_station, self.seat_number,
                       self.departure_time, self.arrival_time]:
            widget.setStyleSheet(input_style)

        if self.passenger:
            self.departure_time.setDateTime(self.passenger.departure_time)
            self.arrival_time.setDateTime(self.passenger.arrival_time)
        else:
            self.departure_time.setDateTime(QDateTime.currentDateTime())
            self.arrival_time.setDateTime(QDateTime.currentDateTime())

        # Добавляем поля в форму
        layout.addRow("Имя:", self.first_name)
        layout.addRow("Фамилия:", self.last_name)
        layout.addRow("Отчество", self.middle_name)
        layout.addRow("Номер паспорта:", self.passport)
        layout.addRow("Номер поезда:", self.train_name)
        layout.addRow("Станция отправления:", self.departure_station)
        layout.addRow("Станция прибытия:", self.arrival_station)
        layout.addRow("Время отправления:", self.departure_time)
        layout.addRow("Время прибытия:", self.arrival_time)
        layout.addRow("Номер места:", self.seat_number)

        # Кнопки
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                min-width: 100px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #43A047;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
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

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)
        layout.addRow(buttons_layout)

    def get_data(self):
        return {
            'first_name': self.first_name.text(),
            'last_name': self.last_name.text(),
            'middle_name': self.middle_name.text(),
            'passport_number': self.passport.text(),
            'train_name': self.train_name.text(),
            'departure_station': self.departure_station.text(),
            'arrival_station': self.arrival_station.text(),
            'departure_time': self.departure_time.dateTime().toPyDateTime(),
            'arrival_time': self.arrival_time.dateTime().toPyDateTime(),
            'seat_number': self.seat_number.text()
        }


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Создаем таблицу
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        headers = ["ID", "Имя", "Фамилия", "Паспорт", "Отчество", "Название поезда", "Станция отправления",
                   "Станция прибытия", "Время отправления", "Время прибытия", "Место"]
        self.table.setHorizontalHeaderLabels(headers)

        # Настраиваем внешний вид таблицы
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                color: black;
                gridline-color: #E0E0E0;
            }
            QTableWidget::item {
                padding: 5px;
                color: black;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #BBDEFB;
                color: black;
            }
        """)

        # Устанавливаем растягивание колонок
        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # Кнопки управления
        button_layout = QHBoxLayout()

        buttons_data = [
            ("Добавить", "#4CAF50", self.add_passenger),
            ("Редактировать", "#2196F3", self.edit_passenger),
            ("Удалить", "#F44336", self.delete_passenger),
            ("Экспорт в Excel", "#FF9800", self.export_to_excel),
            ("Обновить", "#9C27B0", self.load_data)
        ]

        for text, color, callback in buttons_data:
            button = QPushButton(text)
            button.clicked.connect(callback)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                    min-width: 120px;
                    margin: 10px;
                }}
                QPushButton:hover {{
                    background-color: {color}DD;
                }}
                QPushButton:pressed {{
                    background-color: {color}AA;
                }}
            """)
            button_layout.addWidget(button)

        layout.addLayout(button_layout)
        layout.addWidget(self.table)

    def load_data(self):
        with SessionLocal() as db:
            passengers = db.query(Passenger).all()
            self.table.setRowCount(len(passengers))

            for i, passenger in enumerate(passengers):
                self.table.setItem(i, 0, QTableWidgetItem(str(passenger.id)))
                self.table.setItem(i, 1, QTableWidgetItem(passenger.first_name))
                self.table.setItem(i, 2, QTableWidgetItem(passenger.last_name))
                self.table.setItem(i, 3, QTableWidgetItem(passenger.middle_name))
                self.table.setItem(i, 4, QTableWidgetItem(passenger.passport_number))
                self.table.setItem(i, 5, QTableWidgetItem(passenger.train_name))
                self.table.setItem(i, 6, QTableWidgetItem(passenger.departure_station))
                self.table.setItem(i, 7, QTableWidgetItem(passenger.arrival_station))
                self.table.setItem(i, 8, QTableWidgetItem(passenger.departure_time.strftime("%Y-%m-%d %H:%M")))
                self.table.setItem(i, 9, QTableWidgetItem(passenger.arrival_time.strftime("%Y-%m-%d %H:%M")))
                self.table.setItem(i, 10, QTableWidgetItem(passenger.seat_number))

                # Центрируем текст в ячейках
                for j in range(10):
                    item = self.table.item(i, j)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def add_passenger(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить пассажира")
        dialog.setFixedWidth(400)
        layout = QFormLayout()

        # Создаем поля ввода
        fields = {}
        for field in ["Имя", "Фамилия", "Отчество", "Паспорт", "Название поезда", "Станция отправления",
                      "Станция прибытия", "Время отправления", "Время прибытия", "Место"]:
            fields[field] = QLineEdit()
            layout.addRow(field + ":", fields[field])

        # Добавляем кнопку проверки свободных мест
        check_seats_btn = QPushButton("Проверить свободные места")
        check_seats_btn.clicked.connect(lambda: self.check_available_seats(fields["Название поезда"].text()))
        layout.addRow(check_seats_btn)

        # Кнопки
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                with SessionLocal() as db:
                    train = db.query(Train).filter(
                        Train.train_name == fields["Название поезда"].text(),
                    )
                    if not train:
                        QMessageBox.warning(self, "Ошибка", "Поезд не найден")
                        return

                    # Проверяем, не занято ли место
                    existing_seat = db.query(Ticket).filter(
                        Ticket.train_id == train.id,
                        Ticket.seat_number == fields["Место"].text()
                    ).first()

                    if existing_seat:
                        QMessageBox.warning(self, "Ошибка", "Это место уже занято!")
                        return

                    ticket = Ticket(
                        first_name=fields["Имя"].text(),
                        last_name=fields["Фамилия"].text(),
                        middle_name=fields["Отчество"].text(),
                        passport_number=fields["Паспорт"].text(),
                        train_name=fields["Название поезда"].text(),
                        departure_station=fields["Станция отправления"].text(),
                        arrival_station=fields["Станция прибытия"].text(),
                        departure_time=datetime.strptime(fields["Время отправления"].text(), "%Y-%m-%d %H:%M"),
                        arrival_time=datetime.strptime(fields["Время прибытия"].text(), "%Y-%m-%d %H:%M"),
                        seat_number=fields["Место"].text()
                    )
                    db.add(ticket)
                    db.commit()
                    self.load_data()
                    QMessageBox.information(self, "Успех", "Пассажир успешно добавлен")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", str(e))

    def check_available_seats(self, train_name):
        if not train_name:
            QMessageBox.warning(self, "Ошибка", "Введите номер поезда")
            return

        with SessionLocal() as db:
            # Получаем информацию о поезде
            train = db.query(Train).filter(Train.train_number == train_name).first()
            if not train:
                QMessageBox.warning(self, "Ошибка", "Поезд не найден")
                return

            # Получаем занятые места
            occupied_seats = db.query(Passenger.seat_number).filter(
                Passenger.train_number == train_name
            ).all()
            occupied_seats = [seat[0] for seat in occupied_seats]

            # Создаем список свободных мест
            all_seats = set(str(i) for i in range(1, train.total_seats + 1))
            available_seats = all_seats - set(occupied_seats)

            # Показываем диалог со свободными местами
            msg = QMessageBox()
            msg.setWindowTitle("Свободные места")
            msg.setText(f"Свободные места в поезде {train_name}:\n" +
                        ", ".join(sorted(available_seats, key=lambda x: int(x))))
            msg.exec()

    def edit_passenger(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите пассажира для редактирования")
            return

        with SessionLocal() as db:
            passport_number = self.table.item(current_row, 3).text()
            passenger = db.query(Passenger).filter_by(passport_number=passport_number).first()

            dialog = PassengerDialog(self, passenger)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                for key, value in data.items():
                    setattr(passenger, key, value)
                db.commit()
                self.load_data()

    def delete_passenger(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите пассажира для удаления")
            return

        reply = QMessageBox.question(self, "Подтверждение",
                                     "Вы уверены, что хотите удалить этого пассажира?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            with SessionLocal() as db:
                passport_number = self.table.item(current_row, 3).text()
                passenger = db.query(Passenger).filter_by(passport_number=passport_number).first()
                db.delete(passenger)
                db.commit()
                self.load_data()

    def export_to_excel(self):
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Пассажиры"

            # Записываем заголовки
            headers = ["ID", "Имя", "Фамилия", "Паспорт", "Название поезда", "Станция отправления",
                       "Станция прибытия", "Время отправления", "Время прибытия", "Место"]
            for col, header in enumerate(headers, 1):
                ws.cell(row=1, column=col, value=header)

            # Записываем данные
            with SessionLocal() as db:
                passengers = db.query(Passenger).all()
                for row, passenger in enumerate(passengers, 2):
                    ws.cell(row=row, column=1, value=passenger.id)
                    ws.cell(row=row, column=2, value=passenger.first_name)
                    ws.cell(row=row, column=3, value=passenger.last_name)
                    we.cell(row=row, column=4, value=passenger.middle_name)
                    ws.cell(row=row, column=5, value=passenger.passport_number)
                    ws.cell(row=row, column=6, value=passenger.train_name)
                    ws.cell(row=row, column=7, value=passenger.departure_station)
                    ws.cell(row=row, column=8, value=passenger.arrival_station)
                    ws.cell(row=row, column=9, value=passenger.departure_time.strftime("%Y-%m-%d %H:%M"))
                    ws.cell(row=row, column=10, value=passenger.arrival_time.strftime("%Y-%m-%d %H:%M"))
                    ws.cell(row=row, column=11, value=passenger.seat_number)

            # Сохраняем файл
            filename = f"passengers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            wb.save(filename)
            QMessageBox.information(self, "Успех", f"Данные экспортированы в файл {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте данных: {str(e)}")
