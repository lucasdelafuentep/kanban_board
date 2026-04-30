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
        response = await ac.get("/api/board")
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data
    assert "cards" in data
    assert len(data["columns"]) == 5

@pytest.mark.asyncio
async def test_update_board():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Get current board
        response = await ac.get("/api/board")
        board = response.json()
        
        # Modify board
        board["columns"][0]["title"] = "Updated Backlog"
        
        # Update board
        response = await ac.put("/api/board", json=board)
        assert response.status_code == 200
        assert response.json() == {"status": "success"}
        
        # Verify update
        response = await ac.get("/api/board")
        updated_board = response.json()
        assert updated_board["columns"][0]["title"] == "Updated Backlog"
