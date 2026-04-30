import aiosqlite
import os
import json
import asyncio
from .security import get_password_hash

DB_PATH = "kanban.db"

# Default data for new boards
INITIAL_DATA = {
    "columns": [
        {"id": "col-backlog", "title": "Backlog", "cardIds": ["card-1", "card-2"]},
        {"id": "col-discovery", "title": "Discovery", "cardIds": ["card-3"]},
        {
            "id": "col-progress",
            "title": "In Progress",
            "cardIds": ["card-4", "card-5"],
        },
        {"id": "col-review", "title": "Review", "cardIds": ["card-6"]},
        {"id": "col-done", "title": "Done", "cardIds": ["card-7", "card-8"]},
    ],
    "cards": {
        "card-1": {
            "id": "card-1",
            "title": "Align roadmap themes",
            "details": "Draft quarterly themes with impact statements and metrics.",
        },
        "card-2": {
            "id": "card-2",
            "title": "Gather customer signals",
            "details": "Review support tags, sales notes, and churn feedback.",
        },
        "card-3": {
            "id": "card-3",
            "title": "Prototype analytics view",
            "details": "Sketch initial dashboard layout and key drill-downs.",
        },
        "card-4": {
            "id": "card-4",
            "title": "Refine status language",
            "details": "Standardize column labels and tone across the board.",
        },
        "card-5": {
            "id": "card-5",
            "title": "Design card layout",
            "details": "Add hierarchy and spacing for scanning dense lists.",
        },
        "card-6": {
            "id": "card-6",
            "title": "QA micro-interactions",
            "details": "Verify hover, focus, and loading states.",
        },
        "card-7": {
            "id": "card-7",
            "title": "Ship marketing page",
            "details": "Final copy approved and asset pack delivered.",
        },
        "card-8": {
            "id": "card-8",
            "title": "Close onboarding sprint",
            "details": "Document release notes and share internally.",
        },
    },
}

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Create users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        
        # Create boards table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS boards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Ensure MVP user exists with hashed password
        hashed_password = get_password_hash("password")
        await db.execute("""
            INSERT OR IGNORE INTO users (username, password)
            VALUES (?, ?)
        """, ("user", hashed_password))
        
        # If user already existed with plain text password, we should update it to hashed
        # (Only needed if we already had plain text "password" in there)
        await db.execute("""
            UPDATE users SET password = ? WHERE username = ? AND password = ?
        """, (hashed_password, "user", "password"))
        
        # Ensure MVP board exists for the user
        async with db.execute("SELECT id FROM users WHERE username = ?", ("user",)) as cursor:
            user = await cursor.fetchone()
            if user:
                user_id = user[0]
                async with db.execute("SELECT id FROM boards WHERE user_id = ?", (user_id,)) as b_cursor:
                    if not await b_cursor.fetchone():
                        await db.execute("""
                            INSERT INTO boards (user_id, data)
                            VALUES (?, ?)
                        """, (user_id, json.dumps(INITIAL_DATA)))
        
        await db.commit()

async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()
