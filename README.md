[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)


# Задание

1. Реализовать веб-сервис со следующими REST методами:

* Создание пользователя, POST

  * Принимает на вход запросы с именем пользователя;

  * Создаёт в базе данных пользователя заданным именем, так же генерирует уникальный идентификатор пользователя и UUID токен доступа (в виде строки) для данного пользователя;

  * Возвращает сгенерированные идентификатор пользователя и токен.

* Добавление аудиозаписи, POST

  * Принимает на вход запросы, содержащие уникальный идентификатор пользователя, токен доступа и аудиозапись в формате wav;

  * Преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет их в базе данных;

  * Возвращает URL для скачивания записи вида http://host:port/record?id=id_записи&user=id_пользователя.

* Доступ к аудиозаписи, GET

  * Предоставляет возможность скачать аудиозапись по ссылке.

2. Для всех сервисов метода должна быть предусмотрена предусмотрена обработка различных ошибок, возникающих при выполнении запроса, с возвращением соответствующего HTTP статуса.


# Запуск проекта

Клонировать репозиторий:
```bash
git clone git@github.com:MikhailKochetkov/records_for_users.git
```

Создать и активировать виртуальное окружение:
```bash
python -m venv venv
source /venv/Scripts/activate
python -m pip install --upgrade pip
```

Установить зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```

Собрать контейнеры:
```bash
docker-compose up -d --build
```

Остановить контейнеры:
```bash
docker-compose stop
```

Остановить и удалить все контейнеры, образы, volumes:
```bash
docker-compose down -v
```

# Документация API
Документация доступна по эндпойнту:  http://127.0.0.1:8000/docs/

# Примеры запросов

### Создание пользователя

Пример запроса:
```bash
{
  "name": "user1",
  "email": "user1@mail.ru"
}
```

Пример ответа:
```bash
{
  "id": 1,
  "token": "6e223112-58d4-4099-a5c8-6ad67487b3d1"
}
```

### Получение ссылки на аудиозапись

Пример запроса:
```bash
{
  "user_id": 1,
  "token": "6e223112-58d4-4099-a5c8-6ad67487b3d1",
  "audio": "C:/Temp/audio.wav"
}
```

Пример ответа:
```bash
{
  "url": "http://127.0.0.1:8000/record?id=bff281a0-d6a0-49d9-8557-cd5e66828a05&user=4"
}
```

### Скачивание аудиозаписи

Пример запроса:
```bash
id: bff281a0-d6a0-49d9-8557-cd5e66828a05
user: 1
```

Пример ответа:

Ссылка для скачивания файла в формате blob:http://127.0.0.1:8000/ce710c63-b34a-4a0f-9459-eecdd987ba23

Также файл можно скачать, если ввести в адресной строке браузера ссылку http://127.0.0.1:8000/record?id=bff281a0-d6a0-49d9-8557-cd5e66828a05&user=1

# Автор

**Михаил Кочетков** - https://github.com/MikhailKochetkov