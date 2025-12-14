# Recipe Box

API для хранения рецептов.

## Usage
Все команды рекомендуется запускать из virualenv. Все основные команды для взаимодействия с проектом прописаны в Makefile.
### Быстрый старт
```bash
make start
```
Open API находится по адресу: http://127.0.0.1:8000/docs#


### Ритуал перед PR
```bash
make lint
make test
```
или
```bash
make check
```

### Тесты
```bash
make test
```
или
```bash
make coverage
```
<!--

### CI
В репозитории настроен workflow **CI** (GitHub Actions) — required check для `main`.
Badge добавится автоматически после загрузки шаблона в GitHub.

### Контейнеры
```bash
docker build -t secdev-app .
docker run --rm -p 8000:8000 secdev-app
# или
docker compose up --build
```

### Эндпойнты
- `GET /health` → `{"status": "ok"}`
- `POST /items?name=...` — демо-сущность
- `GET /items/{id}`

### Формат ошибок
Все ошибки — JSON-обёртка:
```json
{
  "error": {"code": "not_found", "message": "item not found"}
}
```

См. также: `SECURITY.md`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`. -->
