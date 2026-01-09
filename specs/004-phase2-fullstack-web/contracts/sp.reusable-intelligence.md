# Reusable Intelligence: Phase 2 Todo Web Application

**Feature**: 004-phase2-fullstack-web
**Created**: 2026-01-09
**Purpose**: Define reusable intelligence artifacts - Claude Code Subagents and Agent Skills for AI-native task management.

## Core Principle

Reusable intelligence is a **first-class artifact**, not an afterthought. This specification defines agents and skills that reason over tasks, enabling progressive automation from manual CLI/web operations to autonomous agent-driven workflows.

---

## Subagent Definitions

Subagents are specialized AI agents with clear responsibilities, explicit inputs/outputs, and no overlapping authority. Each subagent owns a distinct domain and cannot access UI directly or mutate database without authorization.

### 1. Task-Planning Agent

**Responsibility**: Reason about task dependencies, ordering, and priority conflicts. Help users organize complex projects into actionable task sequences.

**Domain**: Task decomposition, dependency analysis, priority optimization

**Inputs** (Structured JSON):
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string",
      "priority": "high | medium | low",
      "tags": ["string"],
      "dueDate": "ISO-8601 | null",
      "dependencies": ["task-id-1", "task-id-2"]
    }
  ],
  "goal": "string (e.g., 'Organize tasks for project launch')"
}
```

**Outputs** (Structured JSON):
```json
{
  "sortedTasks": [
    {
      "taskId": "uuid",
      "order": number,
      "reasoning": "string (why this task should come first)"
    }
  ],
  "conflicts": [
    {
      "taskIds": ["uuid", "uuid"],
      "issue": "string (e.g., 'Both tasks are high priority but have conflicting due dates')",
      "recommendation": "string (suggested resolution)"
    }
  ],
  "suggestedDeadlines": [
    {
      "taskId": "uuid",
      "suggestedDueDate": "ISO-8601",
      "reasoning": "string"
    }
  ]
}
```

**Authorization**: Read-only access to task data; cannot mutate tasks without user approval

**Example Use Case**:
- User has 20 tasks for "Website Redesign" project
- User invokes Task-Planning Agent with goal: "Organize tasks by dependency and priority"
- Agent analyzes tasks, identifies "Design mockups" must come before "Implement frontend"
- Agent outputs sorted task list with reasoning, suggests due dates based on dependencies

**Reasoning Process**:
1. Parse task descriptions and tags to infer dependencies
2. Build dependency graph (directed acyclic graph)
3. Detect circular dependencies (error condition)
4. Apply topological sort with priority as tie-breaker
5. Identify conflicts (e.g., high-priority task blocked by incomplete dependency)
6. Generate recommendations

---

### 2. Recurrence Reasoning Agent

**Responsibility**: Calculate next occurrence dates for recurring tasks, handle edge cases (month-end, leap years, daylight saving time), and reason about recurrence pattern appropriateness.

**Domain**: Recurrence logic, date arithmetic, calendar edge cases

**Inputs** (Structured JSON):
```json
{
  "task": {
    "id": "uuid",
    "title": "string",
    "dueDate": "ISO-8601 (required)",
    "recurrence": "daily | weekly | monthly",
    "completedAt": "ISO-8601"
  },
  "timezone": "string (IANA timezone, e.g., 'America/New_York')"
}
```

**Outputs** (Structured JSON):
```json
{
  "nextOccurrence": {
    "dueDate": "ISO-8601",
    "calculationMethod": "string (e.g., 'Added 7 days to original due date')",
    "edgeCasesHandled": ["string (e.g., 'Month-end adjusted: Jan 31 → Feb 28')"]
  },
  "warnings": [
    "string (e.g., 'Recurrence pattern may not fit user intent - suggest weekly instead of daily')"
  ]
}
```

**Authorization**: Read task data, compute next occurrence, return suggestion; cannot mutate database directly

**Example Use Case**:
- User completes recurring task "Monthly report" due Jan 31, 2026
- User invokes Recurrence Reasoning Agent to calculate next occurrence
- Agent determines next due date: Feb 28, 2026 (handles month-end edge case)
- Agent warns: "February has fewer days; adjusted to last day of month"

**Reasoning Process**:
1. Parse original due date and recurrence pattern
2. Calculate next occurrence based on pattern:
   - **Daily**: `original_due_date + 1 day`
   - **Weekly**: `original_due_date + 7 days`
   - **Monthly**: `original_due_date + 1 month`, handle month-end edge case
3. Detect edge cases:
   - Month-end: If original day > days in target month, use last day of month
   - Leap year: Handle Feb 29 correctly
   - Daylight saving: Preserve local time, adjust UTC offset
4. Validate reasonableness (e.g., daily recurrence for annual task is suspicious)
5. Return next occurrence with detailed reasoning

---

### 3. Reminder Evaluation Agent

**Responsibility**: Determine when reminders should trigger, handle missed reminders gracefully, and optimize reminder timing based on user behavior patterns (future: machine learning).

**Domain**: Reminder scheduling, notification timing, user behavior analysis

**Inputs** (Structured JSON):
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "dueDate": "ISO-8601",
      "reminderOffset": number (minutes before due date)
    }
  ],
  "currentTime": "ISO-8601",
  "userTimezone": "string (IANA timezone)"
}
```

**Outputs** (Structured JSON):
```json
{
  "readyReminders": [
    {
      "taskId": "uuid",
      "taskTitle": "string",
      "reminderTime": "ISO-8601",
      "dueDate": "ISO-8601",
      "urgency": "high | medium | low",
      "notificationMethod": "browser | in-app | none"
    }
  ],
  "missedReminders": [
    {
      "taskId": "uuid",
      "taskTitle": "string",
      "reminderTime": "ISO-8601",
      "missedDuration": "ISO-8601 duration (e.g., 'PT2H30M')"
    }
  ]
}
```

**Authorization**: Read-only access to task data; triggers notifications via notification service (no direct DB mutation)

**Example Use Case**:
- User has 5 tasks with reminders scheduled for today
- System polls Reminder Evaluation Agent every 60 seconds
- Agent identifies 2 reminders ready to trigger (within notification window)
- Agent returns list of ready reminders with urgency and recommended notification method

**Reasoning Process**:
1. Calculate reminder time for each task: `reminder_time = due_date - reminder_offset`
2. Compare reminder time with current time:
   - **Ready**: `current_time >= reminder_time AND current_time < due_date`
   - **Missed**: `current_time >= due_date AND reminder not sent`
   - **Pending**: `current_time < reminder_time`
3. Determine urgency:
   - **High**: Due within 1 hour
   - **Medium**: Due within 24 hours
   - **Low**: Due > 24 hours
4. Select notification method (browser preferred, in-app fallback)
5. Return ready and missed reminders with actionable data

---

### 4. Query Interpretation Agent

**Responsibility**: Parse natural language search/filter queries into structured API parameters. Enable users to search tasks using conversational language.

**Domain**: Natural language processing, query parsing, intent recognition

**Inputs** (Structured JSON):
```json
{
  "query": "string (e.g., 'Show me high priority work tasks due this week')",
  "availableTags": ["string (list of known tags for validation)"],
  "currentDate": "ISO-8601"
}
```

**Outputs** (Structured JSON):
```json
{
  "apiParameters": {
    "status": "active | completed | all",
    "priority": "high | medium | low | null",
    "tag": "string | null",
    "search": "string | null",
    "sortBy": "createdAt | dueDate | priority | title",
    "sortOrder": "asc | desc",
    "dueDateRange": {
      "start": "ISO-8601",
      "end": "ISO-8601"
    }
  },
  "interpretation": "string (human-readable interpretation of query)",
  "confidence": number (0.0-1.0, how confident the agent is in this interpretation),
  "alternatives": [
    {
      "apiParameters": { "..." },
      "interpretation": "string",
      "confidence": number
    }
  ]
}
```

**Authorization**: Read-only access to task metadata (tags, priorities); cannot mutate tasks

**Example Use Case**:
- User types: "Show me high priority work tasks due this week"
- Frontend sends query to Query Interpretation Agent
- Agent parses intent:
  - Priority: high
  - Tag: work
  - Due date range: current week (Monday-Sunday)
  - Status: active (implied)
- Agent returns API parameters for `/api/v1/tasks?status=active&priority=high&tag=work&dueDateStart=2026-01-06&dueDateEnd=2026-01-12`

**Reasoning Process**:
1. Tokenize query into keywords
2. Identify intent keywords:
   - **Priority**: "high", "urgent", "critical" → `priority=high`
   - **Status**: "done", "completed" → `status=completed`; "active", "todo" → `status=active`
   - **Tags**: Match against known tags (case-insensitive)
   - **Time**: "this week", "today", "tomorrow", "next month" → calculate date range
   - **Sort**: "oldest first" → `sortBy=createdAt&sortOrder=asc`
3. Build structured API parameters
4. Calculate confidence based on keyword matches (> 0.8 = high confidence)
5. Generate alternative interpretations if ambiguous (e.g., "work" could be verb or tag)

---

## Agent Skills

Agent Skills are reusable, versioned, context-independent workflows that accept structured input and produce structured output. Skills are stored in `/reusable/` or `.specify/skills/` and can be used across CLI, web UI, mobile apps, and future agents.

### Skill 1: Task Decomposition Skill

**Purpose**: Break down a large, complex task into smaller, actionable subtasks.

**Input Schema** (JSON):
```json
{
  "taskTitle": "string (max 200 chars)",
  "taskDescription": "string (max 2000 chars)",
  "targetSubtaskCount": number (suggested number of subtasks, e.g., 5),
  "complexityLevel": "low | medium | high"
}
```

**Output Schema** (JSON):
```json
{
  "subtasks": [
    {
      "title": "string",
      "description": "string",
      "estimatedDuration": "ISO-8601 duration (e.g., 'PT2H' for 2 hours)",
      "dependencies": [number (indices of subtasks this depends on)]
    }
  ],
  "reasoning": "string (why task was decomposed this way)"
}
```

**Reusability Constraints**:
- No hardcoded project-specific terms
- No direct database access
- No UI rendering (pure logic)
- Works with any task regardless of domain

**Versioning**: v1.0.0

**Example Use**:
- CLI: `claude-skill decompose-task --task-title "Launch website" --description "..." --target-count 5`
- Web UI: User right-clicks task, selects "Decompose into subtasks", invokes skill via API
- Agent: Task-Planning Agent invokes this skill internally when detecting complex tasks

**Use Case**:
- User has task: "Launch e-commerce website"
- Skill decomposes into:
  1. Design homepage mockup (2 hours, no dependencies)
  2. Implement frontend (8 hours, depends on #1)
  3. Set up database schema (4 hours, no dependencies)
  4. Implement backend API (8 hours, depends on #3)
  5. Deploy to production (2 hours, depends on #2, #4)

---

### Skill 2: Priority Conflict Resolution Skill

**Purpose**: Detect and resolve conflicts when multiple high-priority tasks have overlapping deadlines.

**Input Schema** (JSON):
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "priority": "high | medium | low",
      "dueDate": "ISO-8601",
      "estimatedDuration": "ISO-8601 duration (optional)"
    }
  ],
  "availableTime": "ISO-8601 duration (e.g., 'PT8H' for 8 hours per day)"
}
```

**Output Schema** (JSON):
```json
{
  "conflicts": [
    {
      "taskIds": ["uuid", "uuid"],
      "conflictReason": "string (e.g., 'Both due tomorrow but require 16 hours total')",
      "severity": "high | medium | low"
    }
  ],
  "resolution": [
    {
      "taskId": "uuid",
      "action": "delay | delegate | split | reduce-scope",
      "newDueDate": "ISO-8601 (if action is delay)",
      "reasoning": "string"
    }
  ]
}
```

**Reusability Constraints**:
- No domain-specific logic (works for any task domain)
- No direct task mutation (returns recommendations only)
- No UI dependencies

**Versioning**: v1.0.0

**Example Use**:
- CLI: `claude-skill resolve-conflicts --tasks tasks.json --available-time PT8H`
- Web UI: Dashboard shows "3 priority conflicts detected", user clicks "Resolve", invokes skill
- Agent: Task-Planning Agent uses this skill internally

**Use Case**:
- User has 3 high-priority tasks all due tomorrow
- Combined estimated duration: 20 hours
- User has 8 hours available
- Skill detects conflict, recommends:
  - Task A: Keep tomorrow (most critical)
  - Task B: Delay by 1 day (less critical)
  - Task C: Split into 2 smaller tasks (half tomorrow, half next day)

---

### Skill 3: Smart Due Date Suggestion Skill

**Purpose**: Suggest realistic due dates for tasks based on priority, estimated duration, and user's existing workload.

**Input Schema** (JSON):
```json
{
  "newTask": {
    "title": "string",
    "priority": "high | medium | low",
    "estimatedDuration": "ISO-8601 duration (optional)"
  },
  "existingTasks": [
    {
      "id": "uuid",
      "dueDate": "ISO-8601",
      "estimatedDuration": "ISO-8601 duration"
    }
  ],
  "userWorkingHours": {
    "hoursPerDay": number (e.g., 8),
    "workingDays": ["monday", "tuesday", "wednesday", "thursday", "friday"]
  }
}
```

**Output Schema** (JSON):
```json
{
  "suggestedDueDate": "ISO-8601",
  "reasoning": "string (e.g., 'Based on your workload, earliest realistic due date is...')",
  "alternatives": [
    {
      "dueDate": "ISO-8601",
      "tradeoff": "string (e.g., 'Earlier date but requires working late')"
    }
  ]
}
```

**Reusability Constraints**:
- No hardcoded business rules (configurable working hours)
- No direct calendar access (works with provided task data only)
- No UI rendering

**Versioning**: v1.0.0

**Example Use**:
- CLI: `claude-skill suggest-due-date --new-task task.json --existing-tasks workload.json`
- Web UI: When creating new task, user clicks "Suggest due date", invokes skill
- Agent: Automatically invoked during task creation if user doesn't specify due date

**Use Case**:
- User creates high-priority task: "Prepare presentation" (estimated 4 hours)
- Skill analyzes existing workload: 6 hours scheduled for today, 8 hours tomorrow
- Skill suggests: Due tomorrow at 5 PM (allows 4 hours after existing 8-hour workload)
- Alternative: Due today at 10 PM (requires working late)

---

### Skill 4: Recurrence Pattern Validator Skill

**Purpose**: Validate whether a chosen recurrence pattern matches user intent and suggest better patterns if mismatch detected.

**Input Schema** (JSON):
```json
{
  "task": {
    "title": "string",
    "description": "string",
    "recurrence": "daily | weekly | monthly",
    "dueDate": "ISO-8601"
  }
}
```

**Output Schema** (JSON):
```json
{
  "isValid": boolean,
  "warnings": ["string (e.g., 'Task title mentions weekly but recurrence is daily')"],
  "suggestions": [
    {
      "recurrence": "daily | weekly | monthly",
      "reasoning": "string"
    }
  ]
}
```

**Reusability Constraints**:
- No hardcoded task titles or descriptions
- No direct task mutation (advisory only)
- No UI dependencies

**Versioning**: v1.0.0

**Example Use**:
- CLI: `claude-skill validate-recurrence --task task.json`
- Web UI: Invoked automatically when user sets recurrence pattern
- Agent: Recurrence Reasoning Agent uses this internally

**Use Case**:
- User creates task: "Weekly team meeting" with recurrence = daily
- Skill detects mismatch: title says "Weekly" but recurrence is daily
- Skill warns: "Task title suggests weekly recurrence but pattern is set to daily"
- Skill suggests: Change recurrence to weekly

---

## Versioning Rules

All Agent Skills MUST follow semantic versioning:

- **MAJOR.MINOR.PATCH**
- **MAJOR**: Breaking changes to input/output schema
- **MINOR**: New optional fields added to input/output schema
- **PATCH**: Bug fixes, documentation updates, no schema changes

**Backward Compatibility**:
- MINOR and PATCH versions must be backward compatible
- Clients using older versions must still work with newer MINOR/PATCH versions
- MAJOR version changes require client updates

**Version Declaration**: Each skill file includes version in metadata:
```json
{
  "skill": "task-decomposition",
  "version": "1.0.0",
  "created": "2026-01-09",
  "lastUpdated": "2026-01-09"
}
```

---

## Cross-Platform Reusability

All subagents and skills MUST be reusable across:

1. **CLI**: Invoke via command-line tool (e.g., `claude-agent task-planning --input tasks.json`)
2. **Web UI**: Invoke via backend API endpoint (e.g., `POST /api/v1/agents/task-planning`)
3. **Mobile Apps**: Same API endpoint as web UI
4. **Future Agents**: Other agents can compose subagents/skills as primitives

**Constraint**: No platform-specific code in subagent/skill logic. All platform differences handled by adapter layer (CLI adapter, API adapter, etc.).

---

## Storage and Organization

### Directory Structure

```
.specify/skills/
├── task-decomposition-v1.0.0.json
├── priority-conflict-resolution-v1.0.0.json
├── smart-due-date-suggestion-v1.0.0.json
└── recurrence-pattern-validator-v1.0.0.json

backend/agents/
├── task_planning_agent.py
├── recurrence_reasoning_agent.py
├── reminder_evaluation_agent.py
└── query_interpretation_agent.py
```

**Skills**: JSON schema files in `.specify/skills/` (versioned filenames)
**Subagents**: Python modules in `backend/agents/` (implement subagent logic, use skills as primitives)

---

## Observability

All subagent invocations and skill executions MUST be logged:

**Log Event Schema**:
```json
{
  "timestamp": "ISO-8601",
  "agentName": "string (e.g., 'task-planning-agent')",
  "skillName": "string (e.g., 'task-decomposition-v1.0.0') | null",
  "inputSummary": "string (brief description of input)",
  "outputSummary": "string (brief description of output)",
  "durationMs": number,
  "success": boolean,
  "error": "string (if success = false)"
}
```

**Logging Destination**: Structured JSON to stdout for centralized collection

---

## Future Enhancements

Phase 3 may add:
- **Learning Agents**: Agents that improve recommendations based on user behavior patterns
- **Chained Agent Workflows**: Multi-step workflows combining multiple subagents
- **User-Defined Skills**: Allow users to define custom skills via UI or DSL
- **Agent Marketplace**: Share and discover community-created skills
