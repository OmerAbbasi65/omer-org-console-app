# Quickstart Guide: Phase 2 Full-Stack Todo Web Application

**Feature**: 004-phase2-fullstack-web
**Created**: 2026-01-09
**Purpose**: Developer onboarding guide for local development setup and common tasks.

---

## Prerequisites

Ensure you have the following installed:

- **Node.js**: v20.x or higher ([Download](https://nodejs.org/))
- **Python**: 3.11 or higher ([Download](https://www.python.org/downloads/))
- **Docker**: Latest version ([Download](https://www.docker.com/products/docker-desktop/))
- **Git**: Latest version
- **Neon Account**: Free account at [neon.tech](https://neon.tech/) for PostgreSQL database

**Verify Installation**:
```bash
node --version  # Should be v20.x or higher
python --version  # Should be 3.11.x or higher
docker --version  # Should be 20.x or higher
```

---

## Initial Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd todoapp
git checkout 004-phase2-fullstack-web
```

### 2. Environment Configuration

Create `.env` files for backend and frontend:

**Backend** (`backend/.env`):
```bash
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@ep-example.us-east-2.aws.neon.tech/todo_db?sslmode=require

# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_RELOAD=true

# CORS (for local development)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Logging
LOG_LEVEL=INFO
```

**Frontend** (`frontend/.env.local`):
```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Environment
NODE_ENV=development
```

**Get Neon Database URL**:
1. Sign up at [neon.tech](https://neon.tech/)
2. Create new project: "Todo App Phase 2"
3. Copy connection string from dashboard
4. Replace `DATABASE_URL` in `backend/.env`

### 3. Install Dependencies

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install
```

---

## Running the Application

### Option 1: Docker Compose (Recommended)

Start all services (backend + frontend + local PostgreSQL):

```bash
docker-compose up
```

Access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

Stop services:
```bash
docker-compose down
```

---

### Option 2: Manual (Development Mode)

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend running at: http://localhost:8000

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

Frontend running at: http://localhost:3000

**Terminal 3 - Database Migrations** (first time only):
```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

---

## Database Setup

### Initial Migration

Create database schema:

```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

### Verify Database Connection

```bash
cd backend
python -c "from src.database import engine; print(engine.url)"
```

Expected output: Your Neon database URL

### Seed Test Data (Optional)

```bash
cd backend
python scripts/seed_test_data.py
```

This creates 10 sample tasks with varying priorities, tags, and due dates.

---

## Running Tests

### Backend Tests

**All Tests**:
```bash
cd backend
source venv/bin/activate
pytest
```

**Unit Tests Only**:
```bash
pytest tests/unit/
```

**Integration Tests Only**:
```bash
pytest tests/integration/
```

**With Coverage**:
```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html  # View coverage report
```

---

### Frontend Tests

**All Tests**:
```bash
cd frontend
npm test
```

**Unit Tests**:
```bash
npm run test:unit
```

**Integration Tests**:
```bash
npm run test:integration
```

**E2E Tests** (requires app running):
```bash
npm run test:e2e
```

**With Coverage**:
```bash
npm test -- --coverage
```

---

## API Examples

### Create Task

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "medium",
  "tags": [],
  "dueDate": null,
  "recurrence": "none",
  "createdAt": "2026-01-09T10:00:00Z",
  "updatedAt": "2026-01-09T10:00:00Z"
}
```

---

### List Tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?status=active&limit=10"
```

---

### Update Task

```bash
curl -X PATCH http://localhost:8000/api/v1/tasks/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "completed": true
  }'
```

---

### Delete Task

```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/550e8400-e29b-41d4-a716-446655440000
```

---

### Filter by Priority and Tag

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?priority=high&tag=work&status=active"
```

---

### Search Tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?search=groceries"
```

---

### Complete Recurring Task (Generates Next Occurrence)

```bash
curl -X POST http://localhost:8000/api/v1/tasks/550e8400-e29b-41d4-a716-446655440000/complete \
  -H "Content-Type: application/json" \
  -d '{
    "completedAt": "2026-01-09T10:30:00Z"
  }'
```

Response includes `nextOccurrence` if task is recurring.

---

## Common Development Tasks

### Add Database Migration

1. Modify SQLModel model in `backend/src/models/`
2. Generate migration:
```bash
cd backend
alembic revision --autogenerate -m "Add reminder_offset field"
```
3. Review generated migration in `backend/alembic/versions/`
4. Apply migration:
```bash
alembic upgrade head
```

---

### Add New API Endpoint

1. **Define Pydantic Models** (`backend/src/models/`):
```python
# backend/src/models/task.py
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
```

2. **Create Service Method** (`backend/src/services/task_service.py`):
```python
def create_task(db: Session, task_data: TaskCreate) -> Task:
    task = Task(**task_data.dict(), id=uuid4())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
```

3. **Add API Route** (`backend/src/api/tasks.py`):
```python
@router.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)
```

4. **Write Tests** (`backend/tests/integration/test_tasks_api.py`):
```python
def test_create_task():
    response = client.post("/api/v1/tasks", json={"title": "Test"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test"
```

---

### Add Frontend Component

1. **Create Component** (`frontend/src/components/TaskCard.tsx`):
```typescript
import { Task } from '@/lib/types';

interface TaskCardProps {
  task: Task;
  onComplete: (id: string) => void;
}

export function TaskCard({ task, onComplete }: TaskCardProps) {
  return (
    <div className="border p-4 rounded">
      <h3>{task.title}</h3>
      <button onClick={() => onComplete(task.id)}>
        {task.completed ? 'Uncomplete' : 'Complete'}
      </button>
    </div>
  );
}
```

2. **Add Tests** (`frontend/src/components/TaskCard.test.tsx`):
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from './TaskCard';

test('renders task title', () => {
  const task = { id: '1', title: 'Test Task', completed: false };
  render(<TaskCard task={task} onComplete={() => {}} />);
  expect(screen.getByText('Test Task')).toBeInTheDocument();
});
```

3. **Use in Page** (`frontend/src/app/page.tsx`):
```typescript
import { TaskCard } from '@/components/TaskCard';

export default async function HomePage() {
  const tasks = await fetchTasks();
  return (
    <div>
      {tasks.map(task => <TaskCard key={task.id} task={task} />)}
    </div>
  );
}
```

---

### Add Agent/Subagent

1. **Create Agent File** (`backend/src/agents/example_agent.py`):
```python
from typing import Dict, Any
from pydantic import BaseModel

class ExampleInput(BaseModel):
    task_id: str
    context: Dict[str, Any]

class ExampleOutput(BaseModel):
    recommendation: str
    confidence: float

def example_agent(input_data: ExampleInput) -> ExampleOutput:
    # Agent reasoning logic here
    return ExampleOutput(recommendation="...", confidence=0.9)
```

2. **Add Agent Tests** (`backend/tests/unit/test_example_agent.py`):
```python
def test_example_agent():
    input_data = ExampleInput(task_id="123", context={})
    result = example_agent(input_data)
    assert result.confidence > 0.8
```

3. **Invoke from Service** (`backend/src/services/task_service.py`):
```python
from src.agents.example_agent import example_agent, ExampleInput

def recommend_action(task_id: str):
    input_data = ExampleInput(task_id=task_id, context={})
    result = example_agent(input_data)
    return result.recommendation
```

---

## Debugging

### Backend Debugging (VS Code)

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["src.main:app", "--reload", "--port", "8000"],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

Set breakpoints in Python code, press F5 to start debugging.

---

### Frontend Debugging (Browser DevTools)

1. Open http://localhost:3000 in Chrome/Firefox
2. Open DevTools (F12)
3. Go to Sources tab
4. Set breakpoints in TypeScript files (mapped via source maps)
5. Trigger action in UI to hit breakpoint

---

### Database Debugging

**View Current Schema**:
```bash
cd backend
psql $DATABASE_URL -c "\d tasks"
```

**View All Tasks**:
```bash
psql $DATABASE_URL -c "SELECT id, title, completed FROM tasks LIMIT 10;"
```

**Reset Database** (WARNING: Deletes all data):
```bash
cd backend
alembic downgrade base
alembic upgrade head
```

---

## Troubleshooting

### "Module not found" error (Python)

```bash
cd backend
pip install -r requirements.txt
```

### "Cannot find module" error (Node.js)

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database connection error

1. Verify `DATABASE_URL` in `backend/.env`
2. Test connection:
```bash
psql $DATABASE_URL -c "SELECT 1;"
```
3. Check Neon dashboard for database status

### CORS error in browser

Verify `ALLOWED_ORIGINS` in `backend/.env` includes `http://localhost:3000`

### Port already in use

**Backend (8000)**:
```bash
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000  # Windows
```

**Frontend (3000)**:
```bash
lsof -ti:3000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :3000  # Windows
```

---

## Useful Commands

### Backend

| Command | Description |
|---------|-------------|
| `uvicorn src.main:app --reload` | Start dev server with auto-reload |
| `alembic upgrade head` | Apply all migrations |
| `alembic downgrade -1` | Rollback last migration |
| `pytest -v` | Run tests with verbose output |
| `black src/` | Format code |
| `ruff check src/` | Lint code |
| `mypy src/` | Type check |

### Frontend

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server |
| `npm run build` | Build production bundle |
| `npm run start` | Start production server |
| `npm test` | Run tests |
| `npm run lint` | Lint code |
| `npm run type-check` | Type check TypeScript |

---

## Next Steps

1. ✅ Setup complete - Application running locally
2. 📖 Read [sp.requirements.md](sp.requirements.md) for feature requirements
3. 🏗️ Read [sp.plan.md](sp.plan.md) for implementation plan
4. ✅ Run tests to verify everything works
5. 🚀 Start implementing Level 1 (Core) features
6. 📋 Run `/sp.tasks` to generate executable task list

---

## Additional Resources

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (Alternative API docs)
- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLModel Docs**: https://sqlmodel.tiangolo.com/
- **Neon Docs**: https://neon.tech/docs
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)

---

**Questions?** Check the troubleshooting section or reach out to the team.
