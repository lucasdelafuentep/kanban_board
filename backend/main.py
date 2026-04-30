from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import json
from .database import init_db, get_db
from .security import verify_password
from .auth import create_access_token, get_current_user
from .ai import call_ai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/api/auth/login")
async def login(data: dict, response: Response, db=Depends(get_db)):
    username = data.get("username")
    password = data.get("password")
    
    async with db.execute("SELECT * FROM users WHERE username = ?", (username,)) as cursor:
        user = await cursor.fetchone()
        if not user or not verify_password(password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_access_token(data={"sub": username})
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=86400, # 1 day
            samesite="lax",
            secure=False,
            path="/",
        )
        return {"status": "success", "username": username}

@app.post("/api/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "success"}

@app.get("/api/auth/check")
async def check_auth(current_user=Depends(get_current_user)):
    return current_user

def apply_ai_actions(board: dict, actions: list):
    if not actions:
        return board
    
    # Deep copy for safety if needed, but dict is enough for now
    new_board = board.copy()
    
    for action in actions:
        action_type = action.get("type")
        
        if action_type == "RENAME_COLUMN":
            col_id = action.get("columnId")
            new_title = action.get("newTitle")
            for col in new_board["columns"]:
                if col["id"] == col_id:
                    col["title"] = new_title
        
        elif action_type == "ADD_CARD":
            col_id = action.get("columnId")
            title = action.get("title")
            details = action.get("details", "")
            card_id = f"card-{os.urandom(4).hex()}"
            new_board["cards"][card_id] = {"id": card_id, "title": title, "details": details}
            for col in new_board["columns"]:
                if col["id"] == col_id:
                    col["cardIds"].append(card_id)
        
        elif action_type == "MOVE_CARD":
            card_id = action.get("cardId")
            target_col_id = action.get("targetColumnId")
            
            # Remove from old column
            for col in new_board["columns"]:
                if card_id in col["cardIds"]:
                    col["cardIds"].remove(card_id)
            
            # Add to new column
            for col in new_board["columns"]:
                if col["id"] == target_col_id:
                    col["cardIds"].append(card_id)
        
        elif action_type == "EDIT_CARD":
            card_id = action.get("cardId")
            title = action.get("title")
            details = action.get("details")
            if card_id in new_board["cards"]:
                if title:
                    new_board["cards"][card_id]["title"] = title
                if details:
                    new_board["cards"][card_id]["details"] = details
        
        elif action_type == "DELETE_CARD":
            card_id = action.get("cardId")
            # Remove from all columns
            for col in new_board["columns"]:
                if card_id in col["cardIds"]:
                    col["cardIds"].remove(card_id)
            # Remove from cards map
            if card_id in new_board["cards"]:
                del new_board["cards"][card_id]
                    
    return new_board

@app.post("/api/ai/chat")
async def ai_chat(data: dict, current_user=Depends(get_current_user), db=Depends(get_db)):
    messages = data.get("messages", [])
    
    # Get current board state for context
    async with db.execute("SELECT data FROM boards WHERE user_id = ?", (current_user["id"],)) as cursor:
        row = await cursor.fetchone()
        board_context = json.loads(row[0]) if row else None
    
    ai_response = await call_ai(messages, board_context)
    
    if "actions" in ai_response and ai_response["actions"] and board_context:
        updated_board = apply_ai_actions(board_context, ai_response["actions"])
        # Persist updated board
        await db.execute("""
            UPDATE boards SET data = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (json.dumps(updated_board), current_user["id"]))
        await db.commit()
    
    return ai_response

@app.get("/api/board")
async def get_board(current_user=Depends(get_current_user), db=Depends(get_db)):
    async with db.execute("""
        SELECT b.data FROM boards b
        WHERE b.user_id = ?
    """, (current_user["id"],)) as cursor:
        row = await cursor.fetchone()
        if row:
            return json.loads(row[0])
        raise HTTPException(status_code=404, detail="Board not found")

@app.put("/api/board")
async def update_board(data: dict, current_user=Depends(get_current_user), db=Depends(get_db)):
    await db.execute("""
        UPDATE boards SET data = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    """, (json.dumps(data), current_user["id"]))
    await db.commit()
    return {"status": "success"}

# Serve frontend static files
if os.path.exists("/app/frontend/out"):
    # Serve specific static assets first
    if os.path.exists("/app/frontend/out/_next/static"):
        app.mount("/_next/static", StaticFiles(directory="/app/frontend/out/_next/static"), name="next-static")
    if os.path.exists("/app/frontend/out/static"):
        app.mount("/static", StaticFiles(directory="/app/frontend/out/static"), name="static")

    @app.get("/")
    def read_root():
        return FileResponse("/app/frontend/out/index.html")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        # Skip API routes - they should be handled above
        if full_path.startswith("api/"):
            return {"error": "API route not found"}
        
        # Try exact file match
        path = f"/app/frontend/out/{full_path}"
        if os.path.exists(path) and os.path.isfile(path):
            return FileResponse(path)
            
        # Try .html suffix (Next.js app router static export convention)
        path_html = f"/app/frontend/out/{full_path}.html"
        if os.path.exists(path_html) and os.path.isfile(path_html):
            return FileResponse(path_html)
            
        return FileResponse("/app/frontend/out/index.html")
else:
    @app.get("/", response_class=HTMLResponse)
    def read_root():
        return """
        <html>
            <head><title>Hello World</title></head>
            <body><h1>Hello, World! FastAPI is running.</h1></body>
        </html>
        """
