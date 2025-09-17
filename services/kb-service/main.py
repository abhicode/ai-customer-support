from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle

DATA_DIR = os.getenv("DATA_DIR", "/data")
INDEX_FILE = os.getenv("INDEX_FILE", os.path.join(DATA_DIR, "faiss.index"))
DOCS_FILE = os.getenv("DOCS_FILE", os.path.join(DATA_DIR, "docs.pkl"))

app = FastAPI(title="Knowledge Base Service")

# init model + FAISS
embedder = SentenceTransformer("all-MiniLM-L6-v2")
vector_dim = 384
if os.path.exists(INDEX_FILE) and os.path.exists(DOCS_FILE):
    index = faiss.read_index(INDEX_FILE)
    with open(DOCS_FILE, "rb") as f:
        documents = pickle.load(f)
else:
    index = faiss.IndexFlatL2(vector_dim)
    documents: List[str] = []


class AddDocsRequest(BaseModel):
    docs: List[str]


class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


@app.post("/add")
def add_docs(req: AddDocsRequest):
    global index, documents
    embeddings = embedder.encode(req.docs, convert_to_numpy=True)
    index.add(embeddings)
    documents.extend(req.docs)

    faiss.write_index(index, INDEX_FILE)
    with open(DOCS_FILE, "wb") as f:
        pickle.dump(documents, f)

    return {"added": len(req.docs), "total_docs": len(documents)}


@app.post("/search")
def search(req: SearchRequest):
    if not documents:
        return {"docs": []}

    query_embedding = embedder.encode([req.query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, req.top_k)
    results = [documents[i] for i in indices[0] if i < len(documents)]
    return {"docs": results}

@app.get("/health")
def health():
    return {"status": "ok"}
