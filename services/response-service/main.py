from fastapi import FastAPI, HTTPException
from rag_pipeline import rag_pipeline
from models import ResponseRequest, ResponsePayload

app = FastAPI(title="Response Generation Service")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/v1/respond", response_model=ResponsePayload)
async def generate_response(req: ResponseRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="text is required")

    intent = (req.intent or "").lower()
    context = req.context or {}

    generated = await rag_pipeline.generate(req.text, intent, context)
    return ResponsePayload(text=generated, source="bot")
