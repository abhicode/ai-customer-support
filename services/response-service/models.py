from pydantic import BaseModel
from typing import Optional

class ResponseRequest(BaseModel):
    text: str
    session_id: Optional[str] = None
    intent: Optional[str] = None
    context: Optional[dict] = {}

class ResponsePayload(BaseModel):
    text: str
    source: str = "bot"