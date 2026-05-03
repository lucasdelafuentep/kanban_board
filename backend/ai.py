import os
import httpx
import json
from typing import List, Dict
from fastapi import HTTPException

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = "openai/gpt-oss-120b:free"

async def call_ai(messages: List[Dict[str, str]], board_context: Dict = None):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not set")

    system_prompt = """You are a helpful project management assistant for a Kanban board app.
You can help the user by renaming columns, adding cards, moving cards, editing cards, or deleting cards.

When you want to perform an action, you MUST return a JSON object in your response. 
Even if you are just chatting, your response must be a JSON object with this structure:
{
  "message": "Your text response to the user here",
  "actions": [
    {
      "type": "RENAME_COLUMN",
      "columnId": "column-id",
      "newTitle": "New Title"
    },
    {
      "type": "ADD_CARD",
      "columnId": "column-id",
      "title": "Card Title",
      "details": "Card Details"
    },
    {
      "type": "MOVE_CARD",
      "cardId": "card-id",
      "targetColumnId": "column-id"
    },
    {
      "type": "EDIT_CARD",
      "cardId": "card-id",
      "title": "New Title",
      "details": "New Details"
    },
    {
      "type": "DELETE_CARD",
      "cardId": "card-id"
    }
  ]
}

If no actions are needed, return an empty list for "actions".
Always provide a friendly "message" explaining what you did.
"""
    if board_context:
        system_prompt += f"\n\nCurrent Kanban Board State:\n{json.dumps(board_context, indent=2)}"
    
    # Prepend system prompt
    full_messages = [{"role": "system", "content": system_prompt}] + messages

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8000", # Required by OpenRouter
                    "X-Title": "Kanban Studio",
                },
                json={
                    "model": MODEL,
                    "messages": full_messages,
                },
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            ai_msg = result["choices"][0]["message"]
            content = ai_msg.get("content", "")
            
            try:
                # Find the first { and last } to extract JSON if there's surrounding text
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    data = json.loads(json_str)
                    return data
                else:
                    return {"message": content, "actions": []}
            except Exception:
                return {"message": content, "actions": []}
        except Exception as e:
            print(f"AI Call failed: {e}")
            return {"error": str(e)}
