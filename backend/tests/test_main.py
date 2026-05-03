import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
import os
import json

@pytest.mark.asyncio
async def test_hello():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI!"}

@pytest.mark.asyncio
async def test_get_board():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Login first to get authenticated
        login_resp = await ac.post("/api/auth/login", json={"username": "user", "password": "password"})
        assert login_resp.status_code == 200
        
        # Now get the board (same client to share cookie)
        response = await ac.get("/api/board")
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data
    assert "cards" in data
    assert len(data["columns"]) == 5

@pytest.mark.asyncio
async def test_update_board():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Login first (same client to share cookie)
        login_resp = await ac.post("/api/auth/login", json={"username": "user", "password": "password"})
        assert login_resp.status_code == 200
        
        # Get current board (same client)
        response = await ac.get("/api/board")
        assert response.status_code == 200
        board = response.json()
        
        # Modify board
        board["columns"][0]["title"] = "Updated Backlog"
        
        # Update board (same client)
        response = await ac.put("/api/board", json=board)
        assert response.status_code == 200
        assert response.json() == {"status": "success"}
        
        # Verify update - get fresh board again
        response = await ac.get("/api/board")
        assert response.status_code == 200
        updated_board = response.json()
        
        # Debug output
        print(f"Updated board columns: {updated_board['columns'][0]}")
        
        assert updated_board["columns"][0]["title"] == "Updated Backlog"