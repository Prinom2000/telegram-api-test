
from fastapi import FastAPI, HTTPException
from telethon import TelegramClient
from pydantic import BaseModel
import os, base64

API_ID   = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION  = os.environ.get("prinom-1")

# Session string থেকে file বানাও
session_bytes = base64.b64decode(SESSION)
with open("session.session", "wb") as f:
    f.write(session_bytes)

app = FastAPI()
client = TelegramClient("session", API_ID, API_HASH)

class MessageRequest(BaseModel):
    to: str
    text: str

@app.on_event("startup")
async def startup():
    await client.start()

@app.post("/send")
async def send_message(req: MessageRequest):
    try:
        await client.send_message(req.to, req.text)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))