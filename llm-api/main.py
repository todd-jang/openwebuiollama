from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    temperature: float = 0.7

@app.post("/v1/chat/completions")
def chat_endpoint(body: ChatRequest):
    user_prompt = next((msg.content for msg in reversed(body.messages) if msg.role == "user"), "")
    response = requests.post("http://ollama:11434/api/generate", json={
        "model": body.model,
        "prompt": user_prompt
    }).json()

    return {
        "id": "chatcmpl-mock",
        "object": "chat.completion",
        "model": body.model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": response.get("response", "")},
                "finish_reason": "stop"
            }
        ]
    }    
@app.get("/v1/models")
def list_models():
    # Ollama에 등록된 모델 목록 요청
    response = requests.get("http://ollama:11434/api/tags").json()
    models = [{"id": m["name"], "object": "model"} for m in response.get("models", [])]
    return {"data": models, "object": "list"}        
