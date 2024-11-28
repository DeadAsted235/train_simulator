# Система управления пассажирами поездов дальнего следования

Приложение для управления информацией о пассажирах поездов дальнего следования с возможностью авторизации и экспорта данных в Excel.

## Возможности

- Авторизация и регистрация пользователей
- Добавление, редактирование и удаление информации о пассажирах
- Просмотр списка пассажиров в табличном виде
- Экспорт данных в Excel
- Современный интерфейс в стиле Material Design

## Требования

- Python 3.8+
- PyQt6
- SQLAlchemy
- openpyxl
- passlib
- qt-material

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## Структура проекта

- `main.py` - главный файл приложения
- `database.py` - настройки базы данных
- `models.py` - модели данных
- `auth.py` - модуль аутентификации
- `ui/` - директория с файлами интерфейса
  - `login.py` - окно входа
  - `register.py` - окно регистрации
  - `main_window.py` - главное окно приложения
