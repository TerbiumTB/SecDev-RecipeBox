# Security Policy

- Пожалуйста, **не** храните ключи/секреты в репозитории.
- Сообщайте об уязвимостях преподавателю/ТА через приватный канал.
- В коде используйте единый формат ошибок (см. README).
- Во время курса используйте **синтетические** данные (без ПДн/платежей).

## Environment Variables

Переменные окружения требуются условно в зависимости от `APP_ENV`:

### Test Mode (`APP_ENV=test`)
**Требуется только:**
- `APP_ENV=test`
- `LOG_LEVEL` (например, `INFO` или `DEBUG`)
- `MOCK_DATABASE_URL` (например, `sqlite:///:memory:`)

**Не требуется:**
- `DATABASE_URL`
- `DB_HOST`, `DB_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

### Production/Development Mode (`APP_ENV != "test"`)
**Требуется:**
- `APP_ENV` (например, `production` или `development`)
- `LOG_LEVEL`
- `DATABASE_URL` (полная строка подключения к PostgreSQL)
- `DB_HOST` (хост PostgreSQL)
- `DB_PORT` (порт PostgreSQL)
- `POSTGRES_USER` (пользователь PostgreSQL)
- `POSTGRES_PASSWORD` (пароль PostgreSQL)
- `POSTGRES_DB` (имя базы данных)

**Не требуется:**
- `MOCK_DATABASE_URL`
