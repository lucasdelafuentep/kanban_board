import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
import json

@pytest.mark.asyncio
async def test_ai_kanban_update():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Login
        await ac.post("/api/auth/login", json={"username": "user", "password": "password"})
        
        # Get initial board
        response = await ac.get("/api/board")
        initial_board = response.json()
        initial_card_count = len(initial_board["cards"])
        
        # Ask AI to add a card
        # We use a very specific prompt to encourage the AI to return the JSON action
        response = await ac.post("/api/ai/chat", json={
            "messages": [{"role": "user", "content": "Add a new card to the Backlog with title 'AI Task' and details 'Created by AI'."}]
        })
        
        assert response.status_code == 200
        ai_data = response.json()
        assert "actions" in ai_data
        
        # Verify the board was updated in the database
        response = await ac.get("/api/board")
        updated_board = response.json()
        assert len(updated_board["cards"]) == initial_card_count + 1
        
        # Find the new card
        new_card = None
        for card in updated_board["cards"].values():
            if card["title"] == "AI Task":
                new_card = card
                break
        assert new_card is not None
        assert new_card["details"] == "Created by AI"
        
        # Now ask AI to delete it
        response = await ac.post("/api/ai/chat", json={
            "messages": [{"role": "user", "content": f"Delete the card with id {new_card['id']}."}]
        })
        assert response.status_code == 200
        
        # Verify it's gone
        response = await ac.get("/api/board")
        final_board = response.json()
        assert new_card["id"] not in final_board["cards"]
