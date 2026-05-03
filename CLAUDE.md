# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Project Management MVP web app with Kanban board functionality and AI-powered chat features. The app uses Next.js for the frontend, FastAPI for the backend, and SQLite for data persistence, all containerized with Docker.

## Key Architecture

### Frontend (Next.js)
- Located in `frontend/` directory
- Kanban board with drag-and-drop functionality using `@dnd-kit`
- 5 fixed columns (Backlog, Discovery, In Progress, Review, Done) with renaming support
- Cards can be added, edited, deleted, and moved between columns
- AI chat sidebar (`AiSidebar.tsx`) integrated with backend AI API
- State management via React hooks with backend API integration
- Testing: Vitest for unit tests, Playwright for e2e tests

### Backend (FastAPI)
- Located in `backend/` directory
- SQLite database with users and boards tables
- JWT-based authentication with hardcoded credentials: `user/password`
- API routes for auth, board CRUD operations, and AI chat
- AI integration with OpenRouter using `openai/gpt-oss-120b:free` model
- Structured AI responses can modify board state (rename columns, add/move/edit/delete cards)
- Serves static Next.js build from `/app/frontend/out` when available

## Development Commands

### Frontend Development
```bash
cd frontend
npm install              # Install dependencies
npm run dev              # Start development server (localhost:3000)
npm run build            # Build for production
npm run start            # Start production server
npm run test:unit        # Run unit tests with Vitest
npm run test:e2e         # Run e2e tests with Playwright
npm run test:all         # Run all tests
```

### Backend Development
```bash
cd backend
pip install -r requirements.txt  # Install dependencies
uvicorn backend.main:app --reload  # Run with auto-reload
```

### Docker Development
```bash
# Build and run
docker-compose up --build

# Stop
docker-compose down
```

### Platform-specific Scripts
- `scripts/start_linux.sh` - Start Docker on Linux
- `scripts/start_mac.sh` - Start Docker on Mac
- `scripts/start_windows.ps1` - Start Docker on Windows
- `scripts/stop.sh` - Stop Docker on Linux/Mac
- `scripts/stop_windows.ps1` - Stop Docker on Windows

## Database Schema

### Users Table
- `id` (INTEGER, PK, AUTOINCREMENT)
- `username` (TEXT, UNIQUE, NOT NULL)
- `password` (TEXT, NOT NULL - bcrypt hashed)

### Boards Table
- `id` (INTEGER, PK, AUTOINCREMENT)
- `user_id` (INTEGER, FK to users.id)
- `data` (TEXT, NOT NULL - JSON serialized Kanban board)
- `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login with username/password (sets JWT cookie)
- `POST /api/auth/logout` - Logout (clears JWT cookie)
- `GET /api/auth/check` - Check current auth status

### Board Operations
- `GET /api/board` - Get current user's board
- `PUT /api/board` - Update board state

### AI Chat
- `POST /api/ai/chat` - Send messages to AI with board context, returns response + optional board updates

## Environment Variables

Required in `.env` file at project root:
- `OPENROUTER_API_KEY` - API key for OpenRouter AI service
- `JWT_SECRET` - Secret key for JWT token signing (optional, defaults to placeholder)
- `CORS_ORIGINS` - Comma-separated list of allowed CORS origins (optional, defaults to "http://localhost:3000")
- `SECURE_COOKIES` - Set to "true" for production (optional, defaults to "false")

## Testing Guidelines

- Frontend tests use Vitest (unit) and Playwright (e2e)
- Backend tests use pytest with pytest-asyncio
- Test files follow `test_*.py` pattern for backend and `*.spec.ts` for frontend
- Run all tests before committing changes

## AI Integration Notes

- AI receives full board context in JSON format
- AI can return structured actions to modify board:
  - `RENAME_COLUMN`: Change column title
  - `ADD_CARD`: Create new card in column
  - `MOVE_CARD`: Move card between columns
  - `EDIT_CARD`: Update card title/details
  - `DELETE_CARD`: Remove card from board
- Actions are applied atomically to board state

## Project Status

All MVP features are complete:
- ✅ Frontend Kanban board with drag-and-drop
- ✅ Authentication system (JWT-based)
- ✅ Backend API with SQLite database
- ✅ AI chat sidebar integration with OpenRouter
- ✅ Docker containerization
- All code review issues resolved