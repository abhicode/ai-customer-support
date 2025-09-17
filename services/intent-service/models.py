from pydantic import BaseModel
from typing import Optional

class IntentRequest(BaseModel):
    text: str
    session_id: Optional[str]

class IntentResponse(BaseModel):
    intents: list
    entities: Optional[dict] = {}
    ml_model_version: Optional[str]