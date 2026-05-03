import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
import json

@pytest.mark.asyncio
async def test_ai_chat_real():
    # This test will actually call OpenRouter if API key is set
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First login to get the cookie
        await ac.post("/api/auth/login", json={"username": "user", "password": "password"})
        
        # Call AI
        response = await ac.post("/api/ai/chat", json={
            "messages": [{"role": "user", "content": "Say hello!"}]
        })
        
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    print(f"AI Response: {data['message']}")

@pytest.mark.asyncio
async def test_ai_chat_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/ai/chat", json={
            "messages": [{"role": "user", "content": "Say hello!"}]
        })
    assert response.status_code == 401
