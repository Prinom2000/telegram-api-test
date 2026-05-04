from fastapi import FastAPI, HTTPException
from telethon import TelegramClient
from pydantic import BaseModel

API_ID   = 31185413          
API_HASH = "a24abffa2e4131c577d0d5d281c79e1f" 
SESSION  = "prinom-1"

app = FastAPI()
client = TelegramClient(SESSION, API_ID, API_HASH)

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