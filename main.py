from fastapi import FastAPI, HTTPException
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from pydantic import BaseModel
import os, httpx, asyncio

API_ID      = int(os.environ.get("API_ID"))
API_HASH    = os.environ.get("API_HASH")
SESSION     = os.environ.get("SESSION_STRING")
N8N_WEBHOOK = os.environ.get("N8N_WEBHOOK_URL")

app = FastAPI()
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

class MessageRequest(BaseModel):
    to: str
    text: str

@app.on_event("startup")
async def startup():
    await client.connect()  # start() এর বদলে connect()

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        sender = await event.get_sender()
        payload = {
            "from_id":   sender.id,
            "from_name": f"{sender.first_name or ''} {sender.last_name or ''}".strip(),
            "username":  sender.username,
            "message":   event.message.text,
            "chat_id":   event.chat_id,
        }
        async with httpx.AsyncClient() as http:
            await http.post(N8N_WEBHOOK, json=payload)

    asyncio.ensure_future(client.run_until_disconnected())

@app.on_event("shutdown")
async def shutdown():
    await client.disconnect()

@app.post("/send")
async def send_message(req: MessageRequest):
    try:
        await client.send_message(req.to, req.text)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}