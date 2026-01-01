# AI-Native Todo Console Application

A command-line task management application built with AI-native design principles, featuring incremental complexity across three feature levels.

## Features

### Level 1 - Basic Task Management (MVP)
- ✅ Add, update, and delete tasks
- ✅ Mark tasks as complete or incomplete
- ✅ View all tasks in a clean tabular format
- ✅ Persistent file-based storage

### Level 2 - Task Organization
- 🏷️ Priority levels (high, medium, low)
- 🔖 Tags for categorization
- 🔍 Search by keyword
- 🎯 Filter by status, priority, or tag
- 📊 Sort by multiple fields

### Level 3 - Advanced Time Management
- 📅 Due dates for tasks
- 🔄 Recurring tasks (daily, weekly, monthly)
- ⏰ Reminder notifications
- ⚠️ Overdue task indicators

## Requirements

- Python 3.11 or higher
- Standard library only (no external dependencies)

## Installation

### Option 1: Install from source (recommended for development)

```bash
# Clone or navigate to the project directory
cd todoapp

# Install in editable mode
pip install -e .
```

### Option 2: Direct execution

```bash
# Run directly with Python
python -m src.main <command> [arguments]
```

## Usage

### Basic Commands (Level 1)

```bash
# Add a new task
todo add "Buy groceries" --description "Milk, eggs, bread"

# List all tasks
todo list

# Update a task
todo update task-1735707600000 --title "Buy groceries and fruits"

# Mark task as complete
todo complete task-1735707600000

# Mark task as incomplete
todo incomplete task-1735707600000

# Delete a task
todo delete task-1735707600000
```

### Organization Commands (Level 2)

```bash
# Add task with priority and tags
todo add "Fix bug in login" --priority high --tags "bug,urgent"

# Set priority for existing task
todo set-priority task-1735707600000 high

# Set tags for existing task
todo set-tags task-1735707600000 "work,urgent"

# Search tasks by keyword
todo search "groceries"

# Filter tasks
todo filter --status active
todo filter --priority high
todo filter --tag urgent
todo filter --status active --priority high --tag work

# Sort tasks
todo sort --by priority
todo sort --by dueDate --order desc
```

### Advanced Commands (Level 3)

```bash
# Add task with due date and recurrence
todo add "Weekly team meeting" --due "2026-01-10T10:00:00" --recurrence weekly

# Add task with reminder
todo add "Doctor appointment" --due "2026-01-15T14:00:00" --remind "2026-01-15T13:30:00"

# Set due date
todo set-due task-1735707600000 "2026-01-20T18:00:00"

# Set recurrence pattern
todo set-recurrence task-1735707600000 daily

# Set reminder time
todo set-reminder task-1735707600000 "2026-01-20T17:00:00"
```

## Data Storage

Tasks are stored in a JSON file at:
- **Linux/Mac**: `~/.todo-data.json`
- **Windows**: `C:\Users\<YourUsername>\.todo-data.json`

The file is human-readable and can be backed up or manually edited if needed.

## Task ID Format

Tasks are assigned unique IDs based on creation timestamp:
- Format: `task-<unix-timestamp-ms>`
- Example: `task-1735707600000`

IDs are chronologically sortable and guaranteed unique for single-user usage.

## Architecture

The application follows a clean layered architecture:

```
┌─────────────────────────────────────┐
│         CLI Layer                   │  ← Command parsing and output
├─────────────────────────────────────┤
│         Domain Layer                │  ← Business logic
├─────────────────────────────────────┤
│         Storage Layer               │  ← JSON persistence
└─────────────────────────────────────┘
```

## Development

### Project Structure

```
todoapp/
├── src/
│   ├── cli/           # CLI argument parsing and formatting
│   ├── domain/        # Task entity and business logic
│   ├── storage/       # File-based persistence
│   ├── reminder/      # Background reminder polling
│   └── main.py        # Application entry point
├── tests/             # Test suite
├── specs/             # Design documentation
└── README.md
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test suite
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/acceptance/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/
```

## Constitutional Principles

This project follows Spec-Driven Development (SDD) with:
1. **Spec-First Development**: All features specified before implementation
2. **AI-Native Design**: Declarative data models and structured formats
3. **Incremental Feature Progression**: Level-gated implementation (Basic → Intermediate → Advanced)
4. **Command-Driven Architecture**: All functionality via explicit CLI commands
5. **Data Model Evolution**: Backward-compatible schema changes
6. **Testing & Validation**: Acceptance criteria for each feature level
7. **Simplicity & YAGNI**: No speculative features, standard library only

## Support

For specification details, see:
- `specs/001-todo-app-full/spec.md` - Complete requirements
- `specs/001-todo-app-full/plan.md` - Implementation plan
- `specs/001-todo-app-full/data-model.md` - Task entity schema
- `specs/001-todo-app-full/contracts/cli-commands.md` - Command syntax

## License

Built following the project constitution at `.specify/memory/constitution.md`
