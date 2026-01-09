# ADR-001: Full-Stack Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-09
- **Feature:** 004-phase2-fullstack-web
- **Context:** Phase 2 requires transition from CLI-based task management to full-stack web application with modern frontend, robust backend, and cloud-native database. Need integrated technology stack that supports progressive feature maturity (Core → Organization → Intelligent), AI-native architecture, and spec-driven development workflow.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Framework choices affect all future development
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Multiple full-stack combinations evaluated
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects frontend, backend, database, deployment
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

**Frontend Stack**:
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5.3+
- **Styling**: TailwindCSS 3+
- **Validation**: Zod
- **Testing**: Jest + React Testing Library + Playwright (E2E)

**Backend Stack**:
- **Framework**: FastAPI 0.109+
- **Language**: Python 3.11+
- **ORM**: SQLModel 0.0.14+
- **Validation**: Pydantic 2.5+
- **Server**: Uvicorn (ASGI)
- **Migrations**: Alembic
- **Testing**: pytest + pytest-asyncio

**Database**:
- **Primary Storage**: Neon PostgreSQL (serverless)
- **Driver**: psycopg3
- **ID Strategy**: UUID v4
- **Time Handling**: Timezone-aware timestamps (UTC storage)

**Infrastructure**:
- **Containerization**: Docker + Docker Compose
- **Local Development**: Docker Compose (backend + frontend + local PostgreSQL)
- **Environment Management**: .env files (separate for backend/frontend)

## Consequences

### Positive

1. **Integrated Developer Experience**:
   - Next.js App Router provides SSR + client-side fetching with single framework
   - FastAPI auto-generates OpenAPI documentation (Swagger UI at /docs)
   - SQLModel unifies Pydantic models and SQLAlchemy ORM (single source of truth)
   - TypeScript + Pydantic provide end-to-end type safety (frontend ↔ API ↔ database)

2. **Performance and Scale**:
   - Next.js SSR delivers fast initial page loads (< 2s p95)
   - FastAPI is one of fastest Python frameworks (async/await native, handles 500 req/s easily)
   - Neon PostgreSQL auto-scales connections, serverless architecture (no manual scaling)
   - TailwindCSS generates minimal CSS (< 50 KB gzipped with purging)

3. **AI-Native Enablement**:
   - FastAPI supports async Python (native integration with Claude SDK, Anthropic API)
   - Pydantic models provide structured JSON for agent inputs/outputs (no free text)
   - Next.js server actions enable seamless agent invocation from UI
   - PostgreSQL stores structured task data queryable by agents

4. **Maintainability**:
   - All components use actively maintained, well-documented frameworks
   - TypeScript + Pydantic catch type errors at compile/runtime (fewer bugs in production)
   - Alembic migrations are version-controlled and reversible (safe schema evolution)
   - Docker Compose provides reproducible local development environment

5. **Community and Ecosystem**:
   - Large communities (Next.js 120K+ GitHub stars, FastAPI 70K+ stars)
   - Rich plugin ecosystems (TailwindCSS plugins, FastAPI middleware, pytest fixtures)
   - Abundant learning resources (official docs, tutorials, Stack Overflow)

### Negative

1. **Complexity**:
   - Multiple languages (TypeScript + Python) require polyglot development team
   - Next.js App Router is newer paradigm (learning curve for developers familiar with Pages Router)
   - SQLModel is less mature than SQLAlchemy (fewer features, smaller community)

2. **Vendor Dependencies**:
   - Neon PostgreSQL is cloud-only (no on-premise option, requires internet connectivity)
   - Next.js is heavily optimized for Vercel deployment (other platforms may have suboptimal performance)
   - Framework lock-in: Migrating away from Next.js or FastAPI is expensive (full rewrite)

3. **Operational Overhead**:
   - Docker Compose requires Docker installed locally (additional setup step)
   - Separate frontend + backend means separate deployment pipelines (more CI/CD complexity)
   - Environment variable management across 2 codebases (frontend/.env.local, backend/.env)

4. **Database Limitations**:
   - Neon free tier has connection limits (max 10 concurrent connections)
   - UUID v4 primary keys cause slight index fragmentation (B-tree performance)
   - No built-in caching layer (future: add Redis for performance)

## Alternatives Considered

### Alternative Stack A: Remix + Prisma + Supabase
- **Frontend**: Remix (React framework with nested routing)
- **Backend**: Integrated with frontend (no separate FastAPI)
- **ORM**: Prisma (TypeScript-native ORM)
- **Database**: Supabase (PostgreSQL with built-in auth/storage)

**Why Rejected**:
- Remix is less mature than Next.js (smaller community, fewer resources)
- No separate backend means harder to add Python-based AI agents (constitutional requirement for AI-native architecture)
- Prisma doesn't support Python (violates polyglot agent requirement)
- Supabase has more features than needed (auth, storage, realtime) - premature complexity for Phase 2

### Alternative Stack B: Create React App + Django + AWS RDS
- **Frontend**: Create React App (CSR only, no SSR)
- **Backend**: Django REST Framework
- **Database**: AWS RDS PostgreSQL

**Why Rejected**:
- Create React App is deprecated (no longer maintained, React team recommends frameworks like Next.js)
- CSR-only means slow initial page loads (no SSR, poor perceived performance)
- Django is heavier than FastAPI (more boilerplate, slower performance)
- AWS RDS requires manual scaling and infrastructure management (more operational complexity than Neon serverless)

### Alternative Stack C: SvelteKit + FastAPI + PlanetScale
- **Frontend**: SvelteKit (Svelte framework with SSR)
- **Backend**: FastAPI (same as chosen)
- **Database**: PlanetScale (MySQL-compatible serverless database)

**Why Rejected**:
- Svelte has smaller ecosystem than React (fewer libraries, smaller talent pool)
- SvelteKit is less mature than Next.js (fewer production deployments)
- PlanetScale uses MySQL (PostgreSQL has better JSON support, full-text search, and advanced features needed for future)
- React/Next.js has stronger AI integration examples and Claude Code support

## References

- Feature Spec: [specs/004-phase2-fullstack-web/sp.requirements.md](../../specs/004-phase2-fullstack-web/sp.requirements.md)
- Implementation Plan: [specs/004-phase2-fullstack-web/sp.plan.md](../../specs/004-phase2-fullstack-web/sp.plan.md)
- Research Decisions: [specs/004-phase2-fullstack-web/sp.research.md](../../specs/004-phase2-fullstack-web/sp.research.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) (v2.0.0 - Technology Stack Requirements)
- Related ADRs: ADR-002 (Data Architecture), ADR-003 (AI-Native Architecture), ADR-004 (API Design)
- Evaluator Evidence: N/A (architectural decision documented in planning phase)
