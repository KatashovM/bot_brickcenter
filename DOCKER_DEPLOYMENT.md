# Docker Deployment с GitHub Actions

## Настройка GitHub Actions

### 1. Создание секретов в GitHub

Для работы GitHub Action необходимо добавить следующие секреты в настройках репозитория:

1. Перейдите в Settings → Secrets and variables → Actions
2. Добавьте следующие секреты:

- `DOCKER_USERNAME` - ваш логин на Docker Hub
- `DOCKER_TOKEN` - токен доступа Docker Hub (рекомендуется вместо пароля)

### 2. Настройка Docker Hub

1. Создайте аккаунт на [Docker Hub](https://hub.docker.com/)
2. Создайте новый репозиторий для вашего бота
3. **Создайте Access Token** (рекомендуется для безопасности):
   - Перейдите в Account Settings → Security
   - Нажмите "New Access Token"
   - Введите описание токена (например, "GitHub Actions")
   - Выберите права доступа: "Read, Write, Delete" для репозиториев
   - Скопируйте созданный токен (он больше не будет показан!)
   - Используйте этот токен как значение для `DOCKER_TOKEN` в GitHub Secrets

**Преимущества использования токена:**
- Более безопасно, чем использование пароля
- Можно отозвать токен в любое время
- Ограниченные права доступа
- Не влияет на основной пароль аккаунта

### 3. Как работает GitHub Action

GitHub Action автоматически:
- Срабатывает при push в ветки `master` или `main`
- Собирает Docker образ для архитектур `linux/amd64` и `linux/arm64`
- Публикует образ в Docker Hub с тегами:
  - `latest` - только для основной ветки (master/main)
  - `{branch_name}` - для всех остальных веток (например, `develop`, `feature/new-feature`)
  - `{branch}-{commit_sha}` - для конкретного коммита
  - `master` или `main` - для соответствующей основной ветки

### 4. Использование образа

После успешной сборки вы можете запустить бота:

**Для продакшена (основная ветка):**
```bash
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN=your_bot_token \
  -e ADMIN_CHAT_ID=your_admin_chat_id \
  -e SMTP_HOST=your_smtp_host \
  -e SMTP_PORT=587 \
  -e SMTP_USER=your_smtp_user \
  -e SMTP_PASSWORD=your_smtp_password \
  -e MAIL_FROM=your_email@example.com \
  -e MAIL_TO=admin@example.com \
  -v bot_data:/app/data \
  your_dockerhub_username/telegram-bot:latest
```

**Для разработки (другие ветки):**
```bash
# Для ветки develop
docker run -d --name telegram-bot-dev your_dockerhub_username/telegram-bot:develop

# Для ветки feature/new-feature
docker run -d --name telegram-bot-feature your_dockerhub_username/telegram-bot:feature/new-feature
```

### 5. Переменные окружения

Обязательные переменные:
- `BOT_TOKEN` - токен бота от BotFather
- `ADMIN_CHAT_ID` - ID чата администратора
- `SMTP_HOST` - SMTP сервер для отправки email
- `SMTP_PORT` - порт SMTP сервера
- `SMTP_USER` - пользователь SMTP
- `SMTP_PASSWORD` - пароль SMTP
- `MAIL_FROM` - email отправителя
- `MAIL_TO` - email получателя

Опциональные переменные:
- `DB_PATH` - путь к файлу базы данных (по умолчанию: `/app/data/bot.db`)

### 6. Volumes

- `/app/data` - директория для хранения базы данных и других данных бота
