from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QDialog, QFormLayout, QLineEdit,
                             QDateTimeEdit, QMessageBox, QHBoxLayout, QHeaderView,
                             QDialogButtonBox, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt, QDateTime
from database import SessionLocal
from models import Passenger, Train, Ticket, Station
import openpyxl
from datetime import datetime


class TicketDialog(QDialog):
    def __init__(self, parent, user, ticket: Ticket=None):
        super().__init__(parent)
        self.user = user

        self.ticket = ticket
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Добавить билет" if not self.ticket else "Редактировать билет")
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
        self.first_name = QLineEdit(self.ticket.passenger.first_name if self.ticket else "", self)
        self.last_name = QLineEdit(self.ticket.passenger.last_name if self.ticket else "", self)
        self.middle_name = QLineEdit(self.ticket.passenger.middle_name if self.ticket else "", self)

        self.series_passport = QLineEdit(self)
        self.series_passport.setInputMask("0000")
        self.series_passport.setText(str(self.ticket.passenger.series_passport) if self.ticket else "")

        self.number_passport = QLineEdit(self)
        self.number_passport.setInputMask("000000")
        self.number_passport.setText(str(self.ticket.passenger.number_passport) if self.ticket else "")

        with SessionLocal() as db:
            trains=[train.train_name for train in db.query(Train).all()]
            self.train_name = QComboBox(self)
            self.train_name.addItems(trains)
            self.train_name.setCurrentIndex(self.train_name.findData(self.ticket.train.train_name) if self.ticket else 0)
            self.train_name.currentTextChanged.connect(self.update_seats_range)
        
            stations = [station.name_station for station in db.query(Station).all()]
            
            self.departure_station = QComboBox(self)
            self.departure_station.addItems(stations)
            self.departure_station.setCurrentIndex(self.departure_station.findData(self.ticket.departure_station.name_station) if self.ticket else 0)
            
            self.arrival_station = QComboBox(self)
            self.arrival_station.addItems(stations)
            self.arrival_station.setCurrentIndex(self.arrival_station.findData(self.ticket.arrival_station.name_station) if self.ticket else 0)

        self.seat_number = QSpinBox(self)
        if self.ticket:
            self.seat_number.setValue(self.ticket.seat_number)

        self.update_seats_range()

        self.departure_time = QDateTimeEdit(self)
        self.arrival_time = QDateTimeEdit(self)

        # Применяем стили
        for widget in [self.first_name, self.last_name, self.middle_name, self.number_passport, self.series_passport,
                       self.train_name, self.departure_station, self.arrival_station, self.seat_number,
                       self.departure_time, self.arrival_time]:
            widget.setStyleSheet(input_style)

        if self.ticket:
            self.departure_time.setDateTime(self.ticket.departure_time)
            self.arrival_time.setDateTime(self.ticket.arrival_time)
        else:
            self.departure_time.setDateTime(QDateTime.currentDateTime())
            self.arrival_time.setDateTime(QDateTime.currentDateTime())

        # Добавляем поля в форму
        layout.addRow("Фамилия:", self.last_name)
        layout.addRow("Имя:", self.first_name)
        layout.addRow("Отчество", self.middle_name)
        layout.addRow("Серия паспорта", self.series_passport)
        layout.addRow("Номер паспорта:", self.number_passport)
        layout.addRow("Поезд:", self.train_name)
        layout.addRow("Станция отправления:", self.departure_station)
        layout.addRow("Станция прибытия:", self.arrival_station)
        layout.addRow("Время отправления:", self.departure_time)
        layout.addRow("Время прибытия:", self.arrival_time)
        layout.addRow("Номер места:", self.seat_number)

        # Добавляем кнопку проверки свободных мест
        check_seats_btn = QPushButton("Проверить свободные места")
        check_seats_btn.clicked.connect(self.check_available_seats)
        layout.addRow(check_seats_btn)

        # Кнопки
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save)
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

    def update_seats_range(self):
        with SessionLocal() as db:
            train = db.query(Train).filter(
                Train.train_name == self.train_name.currentText()
            ).first()

            self.seat_number.setRange(1, train.total_seats if train else 1)

    def check_available_seats(self):
        train_name = self.train_name.currentText()
        if not train_name:
            QMessageBox.warning(self, "Ошибка", "Введите название поезда")
            return

        with SessionLocal() as db:
            # Прверяем наличие поезда
            train = db.query(Train).filter(
                Train.train_name == train_name,
            ).first()

            if not train:
                QMessageBox.warning(self, "Ошибка", "Поезд не найден")
                return

            # Получаем занятые места
            occupied_seats = db.query(Ticket.seat_number).filter(
                Ticket.train_id == train.id
            ).all()

            occupied_seats = set(str(seat[0]) for seat in occupied_seats)
            all_seats = set(str(i) for i in range(1, train.total_seats + 1))

            # Создаем список свободных мест
            available_seats = all_seats - occupied_seats

            # Показываем диалог со свободными местами
            msg = QMessageBox()
            msg.setWindowTitle("Свободные места")
            msg.setText(f"Свободные места в поезде {train_name}:\n" +
                        ", ".join(sorted(available_seats, key=lambda x: int(x))))
            msg.exec()

    def save(self):
        if self.ticket or self.create_ticket():
            self.accept()

    def create_ticket(self) -> bool:
        with SessionLocal() as db:
            # Прверяем наличие поезда
            train = db.query(Train).filter(
                Train.train_name == self.train_name.currentText(),
            ).first()

            if not train:
                QMessageBox.warning(self, "Ошибка", "Поезд не найден")
                return False
            
            seat_number = 0
            try:
                seat_number = int(self.seat_number.text())
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Неправильное место!")
                return False

            # Проверяем, не занято ли место
            existing_seat = db.query(Ticket).filter(
                Ticket.id != self.ticket.id,
                Ticket.train_id == train.id,
                Ticket.seat_number == seat_number,
            ).first() if self.ticket else db.query(Ticket).filter(
                Ticket.train_id == train.id,
                Ticket.seat_number == seat_number,
            ).first()


            if existing_seat:
                QMessageBox.warning(self, "Ошибка", "Это место уже занято!")
                return False

            passenger = db.query(Passenger).filter(
                Passenger.series_passport == self.series_passport.text(),
                Passenger.number_passport == self.number_passport.text(),
            ).first()

            if not passenger:
                passenger = Passenger(
                    first_name=self.first_name.text(),
                    last_name=self.last_name.text(),
                    middle_name=self.middle_name.text(),
                    number_passport=self.number_passport.text(),
                    series_passport=self.series_passport.text(),
                )
                db.add(passenger)
                db.commit()
            
            departure_station = db.query(Station).filter(
                Station.name_station == self.departure_station.currentText(),
            ).first()
            
            if not departure_station:
                QMessageBox.warning(self, "Ошибка", "Станция отправления не найдена!")
                return False

            arrival_station = db.query(Station).filter(
                Station.name_station == self.arrival_station.currentText(),
            ).first()
            
            if not arrival_station:
                QMessageBox.warning(self, "Ошибка", "Станция прибытия не найдена!")
                return False

            ticket = Ticket(
                train_id=train.id,
                passenger_id=passenger.id,
                departure_station_id=departure_station.id,
                arrival_station_id=arrival_station.id,
                departure_time=self.departure_time.dateTime().toPyDateTime(),
                arrival_time=self.arrival_time.dateTime().toPyDateTime(),
                seat_number=self.seat_number.text(),
                cashier_id=self.user.id,
            )
            db.add(ticket)
            db.commit()

            QMessageBox.information(self, "Успех", "Пассажир успешно добавлен")
            return True

    def get_data(self):
        return {
            # 'first_name': self.first_name.text(),
            # 'last_name': self.last_name.text(),
            # 'middle_name': self.middle_name.text(),
            # 'passport_number': self.number_passport.text(),
            # 'series_passport': self.series_passport.text(),
            # 'train_name': self.train_name.text(),
            # 'departure_station': self.departure_station.text(),
            # 'arrival_station': self.arrival_station.text(),
            # 'departure_time': self.departure_time.dateTime().toPyDateTime(),
            # 'arrival_time': self.arrival_time.dateTime().toPyDateTime(),
            # 'seat_number': self.seat_number.text()
        }
