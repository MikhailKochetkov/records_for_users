[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)


# Описание
Сервис позволяет:

* Создавать пользователей

* Сохранять аудиозаписи в формате .wav для каждого пользователя

* Преобразовывать сохраненную аудиозапись в формат .mp3

* Скачивать аудиозапись в формате .mp3 по ссылке

## Как запустить проект:

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

Создать файл .env (шаблон наполнения размещен в файле .env.sample)

### Запуск проекта в режиме разработки:

Установить тестовый режим в настройках проекта (файл settings.py):
```bash
DEV_MODE = True
```

Запустить проект:
```bash
uvicorn main:application
```

### Запуск проекта в Docker (dockerfile):

Установить тестовый режим в настройках проекта (файл settings.py):
```bash
DEV_MODE = True
```

Собрать образ:
```bash
docker build -t api .
```

Запустить контейнер:
```bash
docker run --name records_for_users -it -p 8000:8000 api
```

Получить ID запущенного контейнера:
```bash
docker container ls
```

Остановить контейнер:
```bash
docker container stop <CONTAINER ID>
```

### Запуск проекта в Docker (docker-compose):

Отключить тестовый режим в настройках проекта (файл settings.py):
```bash
DEV_MODE = False
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

## Примеры запросов

### Создание пользователя

Пример запроса:
```bash
{
  "name": "Vasya",
  "email": "vasya@mail.ru"
}
```

Пример ответа:
```bash
{
  "id": 4,
  "token": "6e223112-58d4-4099-a5c8-6ad67487b3d1"
}
```

### Получение ссылки на аудиозапись

Пример запроса:
```bash
{
  "user_id": 4,
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
user: 4
```

Пример ответа:

Ссылка для скачивания файла в формате blob:http://127.0.0.1:8000/ce710c63-b34a-4a0f-9459-eecdd987ba23

Также файл можно скачать, если ввести в адресной строке браузера ссылку http://127.0.0.1:8000/record?id=bff281a0-d6a0-49d9-8557-cd5e66828a05&user=4

# Автор

* **Михаил Кочетков** - https://github.com/MikhailKochetkov