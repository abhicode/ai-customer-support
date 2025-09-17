from fastapi import APIRouter
from models import ConversationRequest, ConversationResponse, BotMessage
import redis.asyncio as redis
import httpx
import uuid
import json

router = APIRouter()

INTENT_SERVICE_URL = "http://intent-service:8000/v1/intent/predict"
RESPONSE_SERVICE_URL = "http://response-service:8000/v1/respond"

redis_client = redis.from_url("redis://redis:6379", decode_responses=True)

@router.post("/v1/conversations", response_model=ConversationResponse)
async def create_or_continue_conversation(req: ConversationRequest):
    session_id = req.session_id or str(uuid.uuid4())
    user_id = req.user_id or str(uuid.uuid4())

    redis_key = f"user:{user_id}:session:{session_id}"

    stored_context = await redis_client.get(redis_key)

    if stored_context:
        try:
            context = json.loads(stored_context)
        except json.JSONDecodeError:
            print("Warning: invalid JSON in Redis")
            context = {}
    else:
        context = {}
        
    if req.context:
        context.update(req.context)

    async with httpx.AsyncClient() as client:
        intent_response = await client.post(INTENT_SERVICE_URL, json={
            "text": req.payload.content,
            "session_id": session_id
        }, timeout=10.0)
        intent_response.raise_for_status()
        intent_data = intent_response.json()
        intent_name = None
        if intent_data.get("intents"):
            intent_name = intent_data["intents"][0]

    entities = intent_data.get("entities", {})
    context.update(entities)

    async with httpx.AsyncClient() as client:
        resp = await client.post(RESPONSE_SERVICE_URL, json={
            "text": req.payload.content,
            "session_id": session_id,
            "intent": intent_name,
            "context": context
        }, timeout=30.0)
        resp.raise_for_status()
        resp_data = resp.json()

    await redis_client.set(redis_key, json.dumps(context), ex=3600)
    
    return ConversationResponse(
        session_id=session_id,
        messages=[BotMessage(source="bot", text=resp_data.get("text", ""))],
        context=context
    )