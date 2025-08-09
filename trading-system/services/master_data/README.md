# Master Data Service

Central repository for reference data such as securities and trading rules.

## Features

- In-memory storage for security master data
- REST API built with FastAPI
- Basic event logging when securities are updated

## Endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET` | `/api/v1/securities` | List all securities |
| `GET` | `/api/v1/securities/{symbol}` | Get details for a symbol |
| `POST` | `/api/v1/securities` | Create or update a security |

Run the service locally:

```bash
uvicorn app.main:app --reload
```
