# P09 - SBOM & SCA Evidence

Этот каталог содержит артефакты, автоматически сгенерированные workflow `.github/workflows/ci-sbom-sca.yml`.

## Структура

- `sbom.json` — Software Bill of Materials в формате CycloneDX JSON, сгенерированный с помощью Syft
- `sca_report.json` — отчёт SCA (Software Composition Analysis) от Grype с найденными уязвимостями
- `sca_summary.md` — краткая сводка по уязвимостям с разбивкой по severity

## Генерация артефактов

Артефакты автоматически генерируются при:
- Push в ветки с изменениями в Python-файлах, requirements*.txt, pyproject.toml
- Ручном запуске workflow через `workflow_dispatch`

## Использование артефактов

1. **Просмотр артефактов**: После успешного выполнения workflow артефакты доступны в разделе "Artifacts" соответствующего workflow run
2. **Локальная генерация**: Для локальной генерации используйте команды из workflow или см. документацию по Syft/Grype
3. **Интеграция в отчёты**: Артефакты используются для формирования раздела DS (Delivery & Security) итогового отчёта

## Инструменты

- **Syft** (vlatest): Генерация SBOM в формате CycloneDX
- **Grype** (vlatest): SCA-сканирование на основе SBOM

## Связь с коммитами

Каждый набор артефактов привязан к конкретному коммиту и workflow run. Ссылки на коммит и workflow run включены в `sca_summary.md`.

## Управление уязвимостями

Найденные уязвимости должны быть обработаны:
- Обновление зависимостей до безопасных версий
- Оформление waivers в `policy/waivers.yml` с обоснованием
