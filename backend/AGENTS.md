# Backend AGENTS.md

## Overview
FastAPI backend for the Project Management MVP, handling authentication, database operations, and AI integration.

## Key Files

### main.py
Entry point with all API routes:
- `/api/hello` - Health check endpoint
- `/api/auth/*` - Authentication endpoints
- `/api/board` - Kanban board CRUD
- `/api/ai/chat` - AI chat with board context
- Static file serving for Next.js frontend

### database.py
- `init_db()` - Initializes SQLite database with users and boards tables
- `get_db()` - Dependency for async database access
- `initial_data` - Default Kanban board structure

### auth.py
- JWT token creation and validation
- `get_current_user()` - Dependency to extract and verify JWT from cookie

### security.py
- `verify_password()` - Bcrypt password verification

### ai.py
- `call_ai()` - Calls OpenRouter API with board context
- Uses `openai/gpt-oss-120b:free` model

## API Endpoints

### Authentication
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/auth/login | Login with username/password |
| POST | /api/auth/logout | Clear JWT cookie |
| GET | /api/auth/check | Return current user info |

### Board Operations
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/board | Get current user's board (auto-creates if missing) |
| PUT | /api/board | Save board state |

### AI Chat
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/ai/chat | Send message, receive response + optional board updates |

## Running

```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## Testing
```bash
pytest tests/
```