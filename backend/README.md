# Todo API - FastAPI Backend

**Phase**: Phase 2 - Level 1 (Core Features)
**Framework**: FastAPI + SQLModel + PostgreSQL

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and set your database URL:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# For Neon PostgreSQL:
# DATABASE_URL=postgresql://user:password@ep-cool-name-123456.region.neon.tech/neondb?sslmode=require
```

### 3. Run the Application

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints (Level 1)

### Tasks

- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks` - Get all tasks
- `GET /api/v1/tasks/{id}` - Get single task
- `PATCH /api/v1/tasks/{id}` - Update task
- `PATCH /api/v1/tasks/{id}/toggle` - Toggle completion
- `DELETE /api/v1/tasks/{id}` - Delete task

### Health

- `GET /` - API information
- `GET /health` - Health check

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── tasks.py          # Task endpoints
│   ├── db/
│   │   └── database.py           # Database connection
│   ├── models/
│   │   └── task.py               # SQLModel schemas
│   ├── config.py                 # Configuration
│   └── main.py                   # FastAPI app
├── .env                          # Environment variables
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Database Schema

### Task Entity (Level 1)

| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | Primary Key |
| title | String(200) | Required |
| description | String(1000) | Optional |
| completed | Boolean | Default: false |
| created_at | DateTime | Auto-generated |
| updated_at | DateTime | Auto-updated |

## Development

### Run with Hot Reload

```bash
uvicorn app.main:app --reload --port 8000
```

### Test API with cURL

```bash
# Create task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'

# Get all tasks
curl http://localhost:8000/api/v1/tasks

# Toggle completion
curl -X PATCH http://localhost:8000/api/v1/tasks/{id}/toggle

# Delete task
curl -X DELETE http://localhost:8000/api/v1/tasks/{id}
```

## Database Migrations

(Alembic migrations will be added in future updates)

For now, tables are auto-created on startup using SQLModel.

## Configuration

All configuration is in `app/config.py` and loaded from environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `FRONTEND_URL` - CORS allowed origin (default: http://localhost:3000)
- `API_V1_PREFIX` - API prefix (default: /api/v1)
- `PROJECT_NAME` - API title
- `ENVIRONMENT` - development/production

## Spec Reference

- **Feature Spec**: `../specs/002-todo-web-app-level1/spec.md`
- **API Contract**: `../specs/002-todo-web-app-level1/contracts/api-endpoints.md`
- **Data Model**: `../specs/002-todo-web-app-level1/contracts/data-model.md`
