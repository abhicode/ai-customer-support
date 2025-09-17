from fastapi import FastAPI, HTTPException
from models import IntentRequest, IntentResponse
from model_loader import get_loader
from ner import extract_entities

app = FastAPI(title="Intent Detection Service")
loader = get_loader()

@app.get("/health")
async def health():
    return {"status": "ok", "model_version": loader.model_version}

@app.post("/v1/intent/predict", response_model=IntentResponse)
async def predict(req: IntentRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    result = loader.predict(req.text)
    intent = result.get("intents")
    ml_model_version = result.get("ml_model_version")

    entities = extract_entities(req.text)

    return IntentResponse(
        intents=intent,
        entities=entities,
        ml_model_version=ml_model_version
    )