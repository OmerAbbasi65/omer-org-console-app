# AI-Native Todo Web Application - Phase 2

**Status**: Level 1 (Core Features) - Implementation Complete ✅
**Architecture**: Full-Stack Web Application
**Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS
**Backend**: FastAPI + SQLModel + PostgreSQL
**Database**: Neon (Serverless PostgreSQL)

## Project Structure

```
todoapp/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/
│   │   │   └── tasks.py         # REST API endpoints
│   │   ├── db/
│   │   │   └── database.py      # Database connection
│   │   ├── models/
│   │   │   └── task.py          # SQLModel schemas
│   │   ├── config.py            # Configuration
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   ├── NEON_SETUP.md           # Neon database guide
│   └── README.md                # Backend documentation
│
├── frontend/                     # Next.js Frontend
│   ├── app/
│   │   ├── actions/
│   │   │   └── tasks.ts         # Server actions (API calls)
│   │   ├── components/
│   │   │   ├── Header.tsx       # App header
│   │   │   ├── TaskForm.tsx     # Add task form
│   │   │   ├── TaskList.tsx     # Task list container
│   │   │   └── TaskItem.tsx     # Individual task item
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Main page
│   │   ├── globals.css          # Global styles
│   │   └── types.ts             # TypeScript types
│   ├── package.json             # Node dependencies
│   ├── .env.example             # Environment template
│   └── README.md                # Frontend documentation
│
├── specs/                        # Phase 2 Specifications
│   └── 002-todo-web-app-level1/
│       ├── spec.md              # Feature specification
│       └── contracts/
│           ├── api-endpoints.md # REST API contract
│           ├── data-model.md    # SQLModel schema
│           └── ui-behavior.md   # Frontend behavior
│
├── src/                          # Phase 1 CLI app (completed)
├── .specify/                     # Spec-Kit Plus framework
└── PHASE2_README.md             # This file
```

## Quick Start

### Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 22+** and npm (for frontend)
- **Neon PostgreSQL account** (free tier available)

### Step 1: Set Up Neon Database

Follow the comprehensive guide:

```bash
# Read the setup guide
cat backend/NEON_SETUP.md

# Or open in your editor
code backend/NEON_SETUP.md
```

**Quick steps**:
1. Go to https://neon.tech and create a free account
2. Create a new project named "todo-app"
3. Copy the PostgreSQL connection string
4. Paste into `backend/.env` file

### Step 2: Set Up Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your Neon connection string

# Run backend
uvicorn app.main:app --reload --port 8000
```

Backend will be running at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Step 3: Set Up Frontend

**In a new terminal:**

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Default API URL is http://localhost:8000 (no changes needed if backend is local)

# Run frontend
npm run dev
```

Frontend will be running at:
- **App**: http://localhost:3000

### Step 4: Test the Application

1. Open http://localhost:3000 in your browser
2. Add a new task using the form
3. View the task in the list
4. Toggle completion by clicking the checkbox
5. Click "Edit" to update the task
6. Click "Delete" to remove the task

## Level 1 Features ✅

### Core Functionality (Implemented)

- ✅ **Add Task**: Create tasks with title and optional description
- ✅ **View Tasks**: Display all tasks in a list
- ✅ **Update Task**: Edit task title and description
- ✅ **Complete Task**: Toggle completion status with checkbox
- ✅ **Delete Task**: Remove tasks with confirmation dialog

### Technical Implementation

#### Backend (FastAPI)
- ✅ RESTful API with 6 endpoints
- ✅ SQLModel for database ORM and validation
- ✅ Neon PostgreSQL for persistent storage
- ✅ Automatic OpenAPI documentation
- ✅ CORS configured for frontend
- ✅ Error handling with standardized responses

#### Frontend (Next.js)
- ✅ App Router architecture
- ✅ TypeScript for type safety
- ✅ Tailwind CSS for styling
- ✅ Component separation (UI, actions, state)
- ✅ Loading states and error handling
- ✅ Responsive design (mobile, tablet, desktop)

## API Endpoints (Level 1)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/tasks` | Create new task |
| GET | `/api/v1/tasks` | Get all tasks |
| GET | `/api/v1/tasks/{id}` | Get single task |
| PATCH | `/api/v1/tasks/{id}` | Update task |
| PATCH | `/api/v1/tasks/{id}/toggle` | Toggle completion |
| DELETE | `/api/v1/tasks/{id}` | Delete task |

Full API documentation: http://localhost:8000/docs

## Database Schema (Level 1)

### Task Entity

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `title` | VARCHAR(200) | NOT NULL | Task title |
| `description` | VARCHAR(1000) | Nullable | Optional description |
| `completed` | BOOLEAN | NOT NULL, Default: false | Completion status |
| `created_at` | TIMESTAMP | NOT NULL | Creation time (UTC) |
| `updated_at` | TIMESTAMP | NOT NULL | Last update time (UTC) |

## Development Workflow

### Running Both Servers

**Terminal 1 (Backend)**:
```bash
cd backend
venv\Scripts\activate  # or source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev
```

### Testing API with cURL

```bash
# Create task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Testing API"}'

# Get all tasks
curl http://localhost:8000/api/v1/tasks

# Toggle completion
curl -X PATCH http://localhost:8000/api/v1/tasks/{task-id}/toggle

# Delete task
curl -X DELETE http://localhost:8000/api/v1/tasks/{task-id}
```

### Viewing Database in Neon Console

1. Go to https://console.neon.tech
2. Select your project
3. Click "Tables" → "tasks"
4. View data in real-time

## Constitutional Compliance ✅

This implementation strictly follows the Phase 2 constitution:

✅ **Spec-First Development**: All features specified before implementation
✅ **Full-Stack Design**: Frontend and backend designed together
✅ **Progressive Feature Maturity**: Level 1 (Core) complete, Level 2 & 3 deferred
✅ **Technology Stack**: Next.js (App Router) + FastAPI + SQLModel + Neon
✅ **Defined Contracts**: API endpoints, data models, and UI behavior all specified
✅ **No Silent Assumptions**: All behaviors explicitly documented

## Specifications Reference

All specifications are located in `specs/002-todo-web-app-level1/`:

- **[spec.md](specs/002-todo-web-app-level1/spec.md)** - Feature requirements and user stories
- **[contracts/api-endpoints.md](specs/002-todo-web-app-level1/contracts/api-endpoints.md)** - REST API specification
- **[contracts/data-model.md](specs/002-todo-web-app-level1/contracts/data-model.md)** - SQLModel schema definition
- **[contracts/ui-behavior.md](specs/002-todo-web-app-level1/contracts/ui-behavior.md)** - Frontend component behavior

## Troubleshooting

### Backend Issues

**"Could not connect to database"**
- Verify Neon connection string in `backend/.env`
- Ensure SSL mode is set to `require`
- Check Neon Console for connection details

**"Module not found"**
- Activate virtual environment: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

**"Port 8000 already in use"**
- Change port: `uvicorn app.main:app --reload --port 8001`
- Update frontend env: `NEXT_PUBLIC_API_URL=http://localhost:8001`

### Frontend Issues

**"Failed to fetch tasks"**
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Verify CORS is configured in backend

**"Module not found"**
- Install dependencies: `npm install`
- Clear cache: `rm -rf .next && npm run dev`

**Tailwind styles not working**
- Restart dev server: `npm run dev`
- Check `tailwind.config.ts` includes correct paths

## Next Steps: Level 2 (Organization)

After Level 1 is validated, Level 2 will add:
- 🏷️ Task priorities (high, medium, low)
- 🔖 Tags for categorization
- 🔍 Search tasks by keyword
- 🎯 Filter by status, priority, or tag
- 📊 Sort by multiple fields

See: `specs/003-todo-web-app-level2/` (to be created)

## Next Steps: Level 3 (Intelligent)

After Level 2 is validated, Level 3 will add:
- 📅 Due dates for tasks
- 🔄 Recurring tasks (daily, weekly, monthly)
- ⏰ Reminder notifications
- ⚠️ Overdue task indicators

See: `specs/004-todo-web-app-level3/` (to be created)

## Success Criteria ✅

Phase 2 Level 1 is considered complete when:

- [x] Full-stack Todo app runs end-to-end
- [x] Specs and implementation match exactly
- [x] All Level 1 features accessible via web UI
- [x] System is extensible for Level 2 & 3
- [ ] End-to-end testing validated by user

## Support

### Documentation
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`
- Neon Setup: `backend/NEON_SETUP.md`
- API Docs: http://localhost:8000/docs

### Specifications
- All specs in `specs/002-todo-web-app-level1/`
- Constitution: `.specify/memory/constitution.md`

## License

See LICENSE file in project root.
