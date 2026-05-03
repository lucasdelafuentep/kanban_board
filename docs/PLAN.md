# High level steps for project


## Part 1: Plan

- [x] Review business requirements and technical decisions in AGENTS.md
- [x] Review existing frontend code and document in frontend/AGENTS.md
- [x] Enrich PLAN.md with detailed substeps, checklists, and success criteria for each part
- [x] Get user approval for the plan before proceeding

**Success Criteria:**
- PLAN.md contains a detailed, actionable checklist for each part
- frontend/AGENTS.md accurately describes the current frontend code
- User has reviewed and approved the plan

**Tests:**
- Manual review of PLAN.md and AGENTS.md for completeness and clarity

---


## Part 2: Scaffolding

- [x] Set up Dockerfile and docker-compose.yml for local development
- [x] Scaffold backend/ with FastAPI app
- [x] Scaffold scripts/ with start/stop scripts for Mac, PC, Linux
- [x] Serve example static HTML from FastAPI at /
- [x] Add a test API route (e.g., /api/hello)
- [x] Validate that the container builds and runs locally

**Success Criteria:**
- Running the container serves static HTML at /
- API route returns expected response

**Tests:**
- Manual: curl or browser to /
- Manual: curl or browser to /api/hello

---


## Part 3: Add in Frontend

- [x] Integrate Next.js frontend build into Docker setup
- [x] Serve built frontend from FastAPI at /
- [x] Validate that the Kanban board demo loads at /
- [x] Ensure all frontend unit and integration tests pass

**Success Criteria:**
- Kanban board is visible at /
- All tests pass

**Tests:**
- `npm run test:unit` (unit)
- `npm run test:e2e` (integration)

---


## Part 4: Add in a fake user sign in experience

- [x] Add login page to frontend
- [x] Require login before showing Kanban board
- [x] Use hardcoded credentials: user / password
- [x] Add logout functionality
- [x] Add tests for login, logout, and access control

**Success Criteria:**
- Kanban board is only visible after login
- Login and logout work as expected
- All tests pass

**Tests:**
- Unit and e2e tests for login/logout

---


## Part 5: Database modeling

- [x] Propose a database schema for Kanban board (supporting multiple users, 1 board per user)
- [x] Use SQLite, store Kanban as JSON
- [x] Document schema and approach in docs/
- [x] Get user sign-off before implementation

**Success Criteria:**
- Schema supports all required features
- Documentation is clear and approved by user

**Tests:**
- Manual review of schema and documentation

---


## Part 6: Backend

- [x] Implement API routes for CRUD operations on Kanban board (per user)
- [x] Ensure database is created if it doesn't exist
- [x] Add backend unit tests for all API routes

**Success Criteria:**
- All API routes work as expected
- Database persists Kanban data
- All backend tests pass

**Tests:**
- Backend unit tests

---


## Part 7: Frontend + Backend

- [x] Update frontend to use backend API for Kanban data
- [x] Ensure board state is persistent per user
- [x] Add tests for frontend-backend integration

**Success Criteria:**
- Kanban board persists changes via API
- All integration tests pass

**Tests:**
- Integration and e2e tests

---


## Part 8: AI connectivity

- [x] Add OpenRouter API key to backend
- [x] Implement backend call to OpenRouter (model: openai/gpt-oss-120b:free)
- [x] Test with a simple "2+2" prompt

**Success Criteria:**
- Backend can call OpenRouter and receive a response

**Tests:**
- Backend test for AI call

---


## Part 9: AI Kanban integration

- [x] Extend backend AI call to include Kanban JSON and user question/history
- [x] Parse AI structured output (response + optional Kanban update)
- [x] Apply Kanban updates if present
- [x] Add tests for structured output handling

**Success Criteria:**
- AI can update Kanban and respond to user
- All tests pass

**Tests:**
- Backend and integration tests

---


## Part 10: AI chat sidebar

- [x] Add sidebar widget to frontend for AI chat
- [x] Integrate with backend AI API
- [x] Display AI responses and update Kanban as needed
- [x] Auto-refresh UI on Kanban update
- [x] Add tests for sidebar and AI integration

**Success Criteria:**
- Sidebar supports full AI chat and Kanban updates
- UI refreshes automatically on changes
- All tests pass

**Tests:**
- Frontend and integration tests