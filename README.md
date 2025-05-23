# Restaurant_test_task
Тестовое задание: Веб-приложение на Fastapi для бронирования столиков в ресторане. Сервис позволяет создавать, просматривать и удалять брони, а также управлять столиками и временными слотами.

### Структура
```
src/
    ├── logging/                # Настройки логирования
    ├── repository/             # Методы для работы с бд
        └── base.py             # Абстрактный базовый класс репозиториев. Базовые crud
    ├── routers/                # Роутеры/Ручки/Эндпоинты
    ├── schemas/                # Модели валидации pydantic
    ├── services/               # Бизнес-логика
    ├── config.py
    ├── db.py                   # engine, session, базовый класс моделей
    ├── dependencies.py  
    ├── enums.py
    ├── main.py
    └── models.py               # Модели базы данных
tests/                       
```
### Стэк
- Fastapi, 
- SQLAlchemy, 
- PostgreSQL, 
- Alembic, 
- Docker

### Для запуска приложения:
1. Создать **.env** с переменными окружения, указанными в **.env.example**
2. Запустить `docker compose up --build` для сборки и развертывания приложения
3. Свагер открываем по адресу http://127.0.0.1:9999/docs


### Тестирование:
- Тесты используют параметры для базы данных из файла **test.env**. Соответственно, название базы данных, имя пользователя и пароль берутся от туда
