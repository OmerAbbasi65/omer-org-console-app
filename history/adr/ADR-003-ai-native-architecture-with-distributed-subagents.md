# ADR-003: AI-Native Architecture with Distributed Subagents

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "AI-Native Architecture" includes subagent boundaries, agent skills, reusable intelligence, observability).

- **Status:** Accepted
- **Date:** 2026-01-09
- **Feature:** 004-phase2-fullstack-web
- **Context:** Constitutional requirement for AI-native architecture with reusable intelligence. Need to implement intelligent task management features (recurring task calculation, reminder evaluation, task planning, query interpretation) using Claude Code Subagents and Agent Skills. Must balance autonomous reasoning (agents make decisions) with system control (agents don't directly mutate database) while ensuring reusability across features and platforms (web UI, CLI, future mobile).

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Agent architecture affects all intelligent features and future AI capabilities
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Centralized vs distributed, hardcoded vs agent-based, multiple integration patterns
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects backend services, API design, frontend features, testing strategy
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Agent Architecture**: Distributed Subagents with Clear Domain Boundaries

**4 Specialized Subagents** (implemented in `backend/src/agents/`):

1. **Task-Planning Agent** (`task_planning_agent.py`):
   - **Domain**: Task dependencies, ordering, priority conflict detection
   - **Inputs**: List of tasks with priorities, due dates, dependencies (JSON)
   - **Outputs**: Sorted task list with reasoning, conflict warnings, deadline suggestions (JSON)
   - **Reusability**: Frontend task organization UI, CLI planning command (future), agent composition

2. **Recurrence Reasoning Agent** (`recurrence_reasoning_agent.py`):
   - **Domain**: Date arithmetic, recurrence pattern calculation, edge case handling (leap years, month-end dates, DST)
   - **Inputs**: Task with recurrence pattern, completion time, timezone (JSON)
   - **Outputs**: Next occurrence due date, calculation method, edge cases handled (JSON)
   - **Reusability**: Backend complete endpoint, reminder service (calculate reminder times), frontend preview

3. **Reminder Evaluation Agent** (`reminder_evaluation_agent.py`):
   - **Domain**: Reminder scheduling, notification timing, missed reminder handling
   - **Inputs**: Tasks with due dates and reminder offsets, current time, user timezone (JSON)
   - **Outputs**: Ready reminders with urgency level and notification method (JSON)
   - **Reusability**: Backend reminders endpoint, frontend polling service, future push notification service

4. **Query Interpretation Agent** (`query_interpretation_agent.py`):
   - **Domain**: Natural language query parsing, intent recognition, API parameter generation
   - **Inputs**: User query string, available tags, current date (JSON)
   - **Outputs**: API parameters (filters, sorting, date ranges), confidence score, alternatives (JSON)
   - **Reusability**: Backend search endpoint, frontend smart search UI, future voice interface

**4 Agent Skills** (versioned JSON schemas in `.specify/skills/`):

1. **task-decomposition-v1.0.0.json**: Break complex task into subtasks with dependencies
2. **priority-conflict-resolution-v1.0.0.json**: Detect and resolve priority conflicts (too many "high" priority tasks)
3. **smart-due-date-suggestion-v1.0.0.json**: Suggest realistic due dates based on workload and complexity
4. **recurrence-pattern-validator-v1.0.0.json**: Validate recurrence pattern matches user intent (detect ambiguous patterns)

**Integration Patterns**:
- **Backend ↔ Agents**: Python imports (no HTTP calls in Phase 2; future: agent API endpoints)
- **Agents ↔ Data**: Read via service layer, no direct database mutations (graceful degradation if agent fails)
- **Frontend ↔ Agents**: Invoke via backend API (agents not directly accessible from frontend)
- **Error Handling**: Agent errors logged but don't crash application (fallback to non-intelligent behavior)

**Observability**:
- All agent invocations logged with structured JSON: `{"timestamp": "...", "agentName": "...", "inputSummary": "...", "outputSummary": "...", "durationMs": 123, "success": true}`
- Logs written to stdout (captured by container orchestrator)
- Future: Integrate with observability platform (DataDog, New Relic)

## Consequences

### Positive

1. **Reusability Across Features and Platforms**:
   - Each subagent can be invoked by multiple features (constitutional requirement: 2+ uses per agent)
   - Web UI, CLI, mobile, future voice interface can all invoke same agents
   - Agent Skills are versioned and portable (can be shared across projects)

2. **Testability and Isolation**:
   - Each agent tested in isolation with JSON input/output contracts (unit tests with pytest)
   - Deterministic outputs for same inputs (no randomness, reproducible tests)
   - Idempotent invocations (safe to call multiple times)
   - Schema validation with Pydantic ensures correctness

3. **Extensibility and Composition**:
   - Add new agents without modifying existing agents (Open/Closed Principle)
   - Agents can invoke other agents (composition pattern for complex reasoning)
   - Future: Agent marketplace for community-created agents

4. **Inspectable Reasoning**:
   - All agent decisions are structured JSON (not free text, fully inspectable)
   - Logging captures agent reasoning for debugging and audit
   - Frontend can display agent reasoning to user (e.g., "Recurrence Reasoning Agent calculated next occurrence using monthly pattern with month-end handling")

5. **Constitutional Compliance**:
   - ✅ AI-Native Architecture requirement met
   - ✅ Behaviors delegated to subagents (not hardcoded)
   - ✅ Reusable intelligence as first-class artifact
   - ✅ Agents use structured JSON (no free text)

### Negative

1. **Complexity**:
   - Distributed agents require coordination and orchestration logic
   - More files to maintain (4 subagent modules + 4 skill schemas)
   - Steeper learning curve for developers unfamiliar with agent-based architecture

2. **Latency**:
   - Agent invocations add latency (Python function call + Pydantic validation + reasoning logic)
   - Expected overhead: 50-200ms per agent invocation (acceptable for Phase 2 scale)
   - Mitigation: Agent results can be cached (future optimization)

3. **Testing Burden**:
   - Each agent requires comprehensive unit tests (happy path + edge cases + error handling)
   - Integration tests must validate agent-assisted flows (e.g., recurring task completion → agent → next occurrence)
   - More test coverage surface area than hardcoded logic

4. **Operational Overhead**:
   - Agent failures must be monitored and alerted (observability platform required for production)
   - Graceful degradation logic needed (fallback when agent fails)
   - Agent performance must be profiled (ensure no latency regressions)

5. **No Direct Database Access**:
   - Agents read data via service layer (additional abstraction)
   - Agents cannot directly mutate database (prevents autonomous database changes)
   - Tradeoff: Safety (controlled mutations) vs simplicity (direct access)

## Alternatives Considered

### Alternative A: Centralized "SmartTaskAgent" (Monolithic Agent)
- **Architecture**: Single agent with multiple methods (plan_tasks, calculate_recurrence, evaluate_reminders, interpret_query)
- **Invocation**: One entry point (`smart_task_agent.py`)

**Why Rejected**:
- Violates Single Responsibility Principle (agent has 4+ distinct purposes)
- Harder to test (cannot isolate recurrence logic from reminder logic)
- Reusability is limited (must invoke entire agent even for single capability)
- Not extensible (adding new capability requires modifying monolithic agent)

### Alternative B: No Agents (Hardcoded Logic)
- **Architecture**: Business logic embedded in service methods (TaskService, ReminderService)
- **Implementation**: Python functions with if/else logic

**Why Rejected**:
- Violates constitutional requirement for AI-native architecture
- Logic is not reusable across platforms (must duplicate in CLI, mobile)
- Logic is not inspectable (buried in code, no structured output)
- Harder to test (logic intertwined with service layer)

### Alternative C: Agent Skills Only (No Subagents)
- **Architecture**: Only versioned Agent Skills (JSON schemas), no autonomous subagents
- **Orchestration**: Backend code orchestrates skills manually

**Why Rejected**:
- Skills are passive (no autonomous reasoning), must be orchestrated by hardcoded logic
- Skills are building blocks, not decision-makers
- Constitutional requirement specifies "subagents" (autonomous reasoning components)
- Both skills and subagents are needed (skills = data structures, subagents = reasoning)

### Alternative D: HTTP-Based Agent Microservices
- **Architecture**: Each agent is separate HTTP service (Docker container)
- **Communication**: Backend invokes agents via REST API

**Why Rejected**:
- Over-engineered for Phase 2 (adds network latency, deployment complexity)
- Python imports are simpler and faster (no HTTP overhead)
- Acceptable for Phase 2 scale (single-server deployment)
- Future: Migrate to microservices when scale requires (Phase 3+)

## References

- Feature Spec: [specs/004-phase2-fullstack-web/sp.requirements.md](../../specs/004-phase2-fullstack-web/sp.requirements.md)
- Reusable Intelligence Spec: [specs/004-phase2-fullstack-web/contracts/sp.reusable-intelligence.md](../../specs/004-phase2-fullstack-web/contracts/sp.reusable-intelligence.md)
- Research Decisions: [specs/004-phase2-fullstack-web/sp.research.md](../../specs/004-phase2-fullstack-web/sp.research.md) (Decision 4)
- Implementation Plan: [specs/004-phase2-fullstack-web/sp.plan.md](../../specs/004-phase2-fullstack-web/sp.plan.md) (Phase 3: Integration & Reusable Intelligence)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (Reusable Intelligence Constitution)
- Related ADRs: ADR-001 (Technology Stack - FastAPI for agent hosting), ADR-002 (Data Architecture - agents use service layer), ADR-004 (API Design - agent invocation via API)
- Evaluator Evidence: N/A (architectural decision documented in planning phase)
