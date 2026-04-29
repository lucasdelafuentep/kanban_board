# High level steps for project


## Part 1: Plan

- [ ] Review business requirements and technical decisions in AGENTS.md
- [ ] Review existing frontend code and document in frontend/AGENTS.md
- [ ] Enrich PLAN.md with detailed substeps, checklists, and success criteria for each part
- [ ] Get user approval for the plan before proceeding

**Success Criteria:**
- PLAN.md contains a detailed, actionable checklist for each part
- frontend/AGENTS.md accurately describes the current frontend code
- User has reviewed and approved the plan

**Tests:**
- Manual review of PLAN.md and AGENTS.md for completeness and clarity

---


## Part 2: Scaffolding

- [ ] Set up Dockerfile and docker-compose.yml for local development
- [ ] Scaffold backend/ with FastAPI app
- [ ] Scaffold scripts/ with start/stop scripts for Mac, PC, Linux
- [ ] Serve example static HTML from FastAPI at /
- [ ] Add a test API route (e.g., /api/hello)
- [ ] Validate that the container builds and runs locally

**Success Criteria:**
- Running the container serves static HTML at /
- API route returns expected response

**Tests:**
- Manual: curl or browser to /
- Manual: curl or browser to /api/hello

---


## Part 3: Add in Frontend

- [ ] Integrate Next.js frontend build into Docker setup
- [ ] Serve built frontend from FastAPI at /
- [ ] Validate that the Kanban board demo loads at /
- [ ] Ensure all frontend unit and integration tests pass

**Success Criteria:**
- Kanban board is visible at /
- All tests pass

**Tests:**
- `npm run test:unit` (unit)
- `npm run test:e2e` (integration)

---


## Part 4: Add in a fake user sign in experience

- [ ] Add login page to frontend
- [ ] Require login before showing Kanban board
- [ ] Use hardcoded credentials: user / password
- [ ] Add logout functionality
- [ ] Add tests for login, logout, and access control

**Success Criteria:**
- Kanban board is only visible after login
- Login and logout work as expected
- All tests pass

**Tests:**
- Unit and e2e tests for login/logout

---


## Part 5: Database modeling

- [ ] Propose a database schema for Kanban board (supporting multiple users, 1 board per user)
- [ ] Use SQLite, store Kanban as JSON
- [ ] Document schema and approach in docs/
- [ ] Get user sign-off before implementation

**Success Criteria:**
- Schema supports all required features
- Documentation is clear and approved by user

**Tests:**
- Manual review of schema and documentation

---


## Part 6: Backend

- [ ] Implement API routes for CRUD operations on Kanban board (per user)
- [ ] Ensure database is created if it doesn't exist
- [ ] Add backend unit tests for all API routes

**Success Criteria:**
- All API routes work as expected
- Database persists Kanban data
- All backend tests pass

**Tests:**
- Backend unit tests

---


## Part 7: Frontend + Backend

- [ ] Update frontend to use backend API for Kanban data
- [ ] Ensure board state is persistent per user
- [ ] Add tests for frontend-backend integration

**Success Criteria:**
- Kanban board persists changes via API
- All integration tests pass

**Tests:**
- Integration and e2e tests

---


## Part 8: AI connectivity

- [ ] Add OpenRouter API key to backend
- [ ] Implement backend call to OpenRouter (model: openai/gpt-oss-120b:free)
- [ ] Test with a simple "2+2" prompt

**Success Criteria:**
- Backend can call OpenRouter and receive a response

**Tests:**
- Backend test for AI call

---


## Part 9: AI Kanban integration

- [ ] Extend backend AI call to include Kanban JSON and user question/history
- [ ] Parse AI structured output (response + optional Kanban update)
- [ ] Apply Kanban updates if present
- [ ] Add tests for structured output handling

**Success Criteria:**
- AI can update Kanban and respond to user
- All tests pass

**Tests:**
- Backend and integration tests

---


## Part 10: AI chat sidebar

- [ ] Add sidebar widget to frontend for AI chat
- [ ] Integrate with backend AI API
- [ ] Display AI responses and update Kanban as needed
- [ ] Auto-refresh UI on Kanban update
- [ ] Add tests for sidebar and AI integration

**Success Criteria:**
- Sidebar supports full AI chat and Kanban updates
- UI refreshes automatically on changes
- All tests pass

**Tests:**
- Frontend and integration tests