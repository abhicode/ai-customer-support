from pydantic import BaseModel
from typing import Optional, Dict, List

class Payload(BaseModel):
    content: str

class ConversationRequest(BaseModel):
    session_id: Optional[str]
    user_id: str
    payload: Payload
    context: Optional[Dict] = {}

class BotMessage(BaseModel):
    source: str
    text: str
    metadata: Dict = {}

class ConversationResponse(BaseModel):
    session_id: str
    status: str = "ok"
    messages: List[BotMessage]
    context: Optional[Dict] = {}