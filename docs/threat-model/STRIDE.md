# STRIDE-угрозы

| Поток/Элемент | Угроза (STRIDE) | Риск | Контроль | Ссылка на NFR | Проверка/Артефакт |
|---------------|------------------|------|-----------|---------------|-------------------|
| F1 /login | **S: Spoofing** (подмена пользователя) | R1 | MFA, Argon2id, rate-limit | NFR-01, NFR-04 | e2e + ZAP baseline |
| F2 /recipes | **I: Information disclosure** | R2 | Единый формат ошибок AppError без стэктрейсов | NFR-02 | Контрактные тесты ошибок |
| F3 AuthService | **T: Tampering** (изменение токена) | R3 | Подпись JWT HS256, exp+aud | NFR-01 | JWT unit tests |
| F4 RecipeService | **R: Repudiation** | R4 | Аудит логов, trace-id в ответах | NFR-07 | Loki/Grafana dashboards |
| F5 SQL (Auth DB) | **I: Information disclosure** | R5 | Шифрование паролей Argon2, ограничение ролей | NFR-06 | DB permissions check |
| F6 SQL (Recipe DB) | **D: Denial of Service** | R6 | Пулы соединений, retry/backoff | NFR-03 | Locust load test |
| F7 Backup | **E: Elevation of privilege** | R7 | Шифрование бэкапов, ограничение доступа | NFR-08 | CI: verify encryption |
| F8 Ошибка логина | **I: Info Disclosure** | R8 | Не выдавать различий между invalid user/password | NFR-02 | Негативные тесты |
| API компонент | **S: Spoofing / T: Tampering** | R9 | CORS, HTTPS-only, secure cookies | NFR-05 | Security headers test |
