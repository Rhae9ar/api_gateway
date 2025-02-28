# API-шлюз с rate limiting и кэшированием

Этот проект представляет собой API-шлюз, разработанный с использованием FastAPI, Redis и Nginx. Он реализует ограничение количества запросов (rate limiting), кэширование ответов и проксирование запросов к бэкенду.

## Описание

API-шлюз выполняет следующие функции:

  * Ограничение количества запросов на пользователя (rate limiting).
  * Кэширование ответов от API для уменьшения нагрузки (Redis).
  * Проксирование запросов к бэкенду через Nginx.
  * Поддержка аутентификации пользователей (JWT).

## Технологии

  * FastAPI
  * Redis
  * Nginx
  * Docker
  * PyJWT
  * Uvicorn


## Запуск проекта

1.  Клонируйте репозиторий


2.  Создайте виртуальное окружение и установите зависимости:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    # venv\Scripts\activate  # Для Windows
    pip install -r requirements.txt
    ```

3.  Запустите Docker Compose:

    ```bash
    docker-compose up --build
    ```

4.  API-шлюз будет доступен по адресу `http://localhost`.

## Настройка

  * Настройки Redis хранятся в файле `.env`.
  * Конфигурация Nginx находится в файле `nginx.conf`.
  * Секретный ключ JWT также хранится в `.env`.

## Тестирование

Для запуска тестов выполните следующую команду:

```bash
pytest
```

## Документация

Документация к API доступна по адресу `http://localhost/docs`.

## Примеры запросов

  * Получение токена:

    ```bash
    curl -X POST "http://localhost/token" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "username=testuser&password=password"
    ```

  * Защищенный эндпоинт:

    ```bash
    curl -X GET "http://localhost/protected" -H "accept: application/json" -H "Authorization: Bearer <token>"
    ```

## Лицензия

[MIT](https://www.google.com/url?sa=E&source=gmail&q=LICENSE)


