# Atomic Habits Tracker
Трекер полезных привычек — бэкенд-приложение на Django REST Framework, вдохновленное книгой Джеймса Клира «Атомные привычки».

### Технологический стек
* Backend: Django 4.2 + DRF

* Database: PostgreSQL

* Async Tasks: Celery + Redis

* Web Server: Nginx

* Containerization: Docker + Docker Compose

* CI/CD: GitHub Actions

* Auth: JWT

* Notifications: Telegram Bot

## Быстрый старт (разработка)
### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/atomic-habits.git
cd atomic-habits
```
### 2. Настройка окружения 
Создайте .env на основе .env.example:
```bash
cp .env.example .env
```
* Отредактируйте .env (укажите свои SECRET_KEY, DB_*, TELEGRAM_BOT_TOKEN).

### 3. Запуск через Docker (разработка)
```bash
docker-compose up --build
```
Приложение будет доступно на: http://localhost:8000

## Production-развертывание
### 1. Настройка сервера
* Установите Docker и Docker Compose:
```bash
sudo apt update && sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```
* Скопируйте проект на сервер:
```bash
scp -r . user@your-server:/opt/atomic-habits
```
## CI/CD (GitHub Actions)
При пуше в ветку main автоматически:

Запускаются тесты

Собираются Docker-образы

Проект деплоится на сервер

Требуемые Secrets в GitHub:
SSH_HOST — IP сервера

SSH_USER — пользователь

SSH_PRIVATE_KEY — приватный SSH-ключ

## API Endpoints
Метод	Эндпоинт	Описание
POST	/api/auth/register/	Регистрация пользователя
POST	/api/auth/login/	Авторизация (JWT)
GET	/api/habits/	Список привычек пользователя
POST	/api/habits/	Создание привычки
GET	/api/public-habits/	Публичные привычки
Документация API:

* Swagger: /swagger/

* ReDoc: /redoc/

## Интеграция с Telegram
1. Создайте бота через @BotFather.
2. Укажите токен в .env: TELEGRAM_BOT_TOKEN=your_bot_token 
3. Привяжите аккаунт командой /connect в боте.

## Команды для управления
### Миграции
```bash
docker-compose exec django python manage.py migrate
```
### Создание суперпользователя
```bash
docker-compose exec django python manage.py createsuperuser
```
### Запуск Celery
```bash
docker-compose exec celery celery -A config worker -l info
```
## Тестирование
```bash
docker-compose exec django python manage.py test
```
## Лицензия
MIT License.