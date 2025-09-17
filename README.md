# AI Customer Support Chatbot  

An end-to-end AI-powered support system built with **FastAPI**, **MLflow**, **FAISS**, and **Next.js**.  
The chatbot handles customer queries, retrieves answers from a knowledge base, tracks conversation context, and connects to human support when needed.  

<video src="https://github.com/user-attachments/assets/51b0335f-84f8-4342-a422-5b7ed1636ca2" autoplay muted loop controls width="600"></video>

## Features  
- **Conversational AI**: Handles customer queries via `/v1/conversations`.  
- **Knowledge Base (`FAISS`)**: Stores documents and provides context-aware responses.  
- **Intent Recognition**: MLflow-hosted Logistic Regression model to classify intents.  
- **Entity Extraction**: `spaCy-based NER` for extracting order IDs, dates, products, etc.  
- **Redis Session Store**: Keeps conversation context for personalized follow-ups.  
- **Frontend (`Next.js` + `MUI`)**: Responsive chat UI for interaction.  
- **Dockerized Microservices**: Orchestrator, Intent Service, Response Service, KB Service, MLflow, and Redis.  

## Architecture  
1. **Frontend (`Next.js`)** → Calls `orchestrator` API.  
2. **Orchestrator (`FastAPI`)** → Routes queries to intent-service, response-service, and kb-service.  
3. **Intent Service** → Uses `MLflow model` for intent classification.  
4. **Response Service** → Generates AI responses (OpenAI API).  
5. **KB Service** → Manages `FAISS vector DB` and document embeddings.  
6. **Redis** → Stores session context.  

## Tech Stack  
- **Backend**: `FastAPI`, `Redis`, `MLflow`, `FAISS`, `spaCy`  
- **Frontend**: `Next.js`, `Material UI`  
- **AI Models**: `Sentence Transformers`, `Logistic Regression (MLflow)`, `OpenAI GPT`  
- **Deployment**: `Docker Compose` 

## Getting Started  
### Prerequisites  
- `Docker` & `Docker Compose` installed  
- OpenAI API key (`OPENAI_API_KEY`)  

### Run Services
#### 1. Change current directory to "infra"
```bash
cd infra
```
#### 2. Run MLflow
```bash
docker-compose up -d --build mlflow
```
runs on http://localhost:5000/

#### 3. Run Logistic Regression Trainer
```bash
docker-compose run --rm trainer
```

#### 4. Go to MLflow UI and promote the model to "Production"

#### 5. Run the frontend container, which will run the rest of the containers
```bash
docker-compose up -d --build frontend
```
Runs on http://localhost:3000
