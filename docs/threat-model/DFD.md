# Data Flow Diagram (DFD)

## Основной сценарий: взаимодействие клиента с API рецептов


```mermaid
flowchart LR
    U["Пользователь (браузер/клиент)"] -->|F1: HTTPS REST /login| API[FastAPI Backend]
    U -->|F2: HTTPS REST /recipes| API

    subgraph Edge[Trust Boundary: Edge Layer]
        API -->|F3: async call| AUTH[Auth Service]
        API -->|F4: REST/gRPC| REC[Recipe Service]
    end

    subgraph Core[Trust Boundary: Core Layer]
        AUTH -->|"F5: SQL (Argon2 hash lookup)"| DB[(User DB)]
        REC -->|"F6: SQL (CRUD recipes)"| DB
    end

    subgraph Data[Trust Boundary: Data Layer]
        DB -->|F7: File backup| BACKUP[(Encrypted Storage)]
    end


    API -.->|"F9: Ошибка (ApiError)"| U

    style Edge stroke:#3B82F6,stroke-width:2px
    style Core stroke:#10B981,stroke-width:2px
    style Data stroke:#F59E0B,stroke-width:2px
```

| ID | Поток/действие        | Канал                  | Краткое описание                  |
| -- | --------------------- | ---------------------- | --------------------------------- |
| F1 | POST /login           | HTTPS                  | Передача логина и пароля          |
| F2 | GET /recipes          | HTTPS                  | Получение списка рецептов         |
| F3 | API → AuthService     | внутренний async вызов | Проверка JWT/сессии               |
| F4 | API → RecipeService   | gRPC/REST              | CRUD операции над рецептами       |
| F5 | AuthService → UserDB  | SQL                    | Проверка пароля                   |
| F6 | RecipeService → DB    | SQL                    | Чтение/запись рецептов            |
| F7 | DB → Backup           | файловый канал         | Бэкап базы данных                 |
| F9 | Ответ с ошибкой       | HTTPS                  | Формат JSON, обёрнутый в ApiError |
