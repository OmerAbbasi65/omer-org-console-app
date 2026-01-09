# Todo Frontend - Next.js Application

**Phase**: Phase 2 - Level 1 (Core Features)
**Framework**: Next.js 14 (App Router) + TypeScript + Tailwind CSS

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local` file:

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run the Application

```bash
npm run dev
```

The app will be available at http://localhost:3000

## Features (Level 1)

- ✅ Add new tasks
- ✅ View all tasks
- ✅ Update task title and description
- ✅ Mark tasks as complete/incomplete
- ✅ Delete tasks with confirmation

## Project Structure

```
frontend/
├── app/
│   ├── actions/
│   │   └── tasks.ts              # Server actions (API calls)
│   ├── components/
│   │   ├── Header.tsx            # App header
│   │   ├── TaskForm.tsx          # Add new task form
│   │   ├── TaskList.tsx          # Display all tasks
│   │   └── TaskItem.tsx          # Single task item
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Main page
│   ├── globals.css               # Global styles
│   └── types.ts                  # TypeScript types
├── public/                       # Static files
├── .env.example                  # Environment template
├── .env.local                    # Environment variables (gitignored)
├── next.config.js                # Next.js configuration
├── tailwind.config.ts            # Tailwind configuration
├── tsconfig.json                 # TypeScript configuration
├── package.json                  # Dependencies
└── README.md                     # This file
```

## Component Architecture

As defined in: `../specs/002-todo-web-app-level1/contracts/ui-behavior.md`

```
┌─────────────────────────────────────────┐
│  UI Components (app/components/)        │  ← Presentational only
├─────────────────────────────────────────┤
│  Server Actions (app/actions/)          │  ← API calls
├─────────────────────────────────────────┤
│  State Management (React hooks/context) │  ← Client state
└─────────────────────────────────────────┘
```

## Development

### Run with Hot Reload

```bash
npm run dev
```

### Build for Production

```bash
npm run build
npm start
```

### Lint Code

```bash
npm run lint
```

## Configuration

- **NEXT_PUBLIC_API_URL**: Backend API URL (default: http://localhost:8000)

## Spec Reference

- **Feature Spec**: `../specs/002-todo-web-app-level1/spec.md`
- **API Contract**: `../specs/002-todo-web-app-level1/contracts/api-endpoints.md`
- **UI Behavior**: `../specs/002-todo-web-app-level1/contracts/ui-behavior.md`

## Next Steps

1. Start backend API: `cd ../backend && uvicorn app.main:app --reload`
2. Start frontend: `npm run dev`
3. Open http://localhost:3000
