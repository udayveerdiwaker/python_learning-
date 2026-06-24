import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from typing import List, Dict

import models
import schemas
from database import engine, get_db, SessionLocal

# Create DB Tables on Startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advanced Chat API")

# Add CORS middleware to allow connection from file:// protocol
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        # Maps room names to lists of active WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections:
            if websocket in self.active_connections[room]:
                self.active_connections[room].remove(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def broadcast(self, message: dict, room: str):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                try:
                    await connection.send_json(message)
                except Exception:
                    # Connection might have died in the meantime
                    pass

    async def broadcast_global(self, message: dict):
        # Send to all connected WebSockets in all rooms
        for room, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

manager = ConnectionManager()

# Serve Frontend
@app.get("/", response_class=HTMLResponse)
def get_chat_interface():
    # Read and serve the index.html template
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat interface index.html not found."
        )

# REST API Endpoints
@app.get("/messages", response_model=List[schemas.MessageResponse])
def get_messages(
    room: str = "general",
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    messages = db.query(models.Message)\
        .filter(models.Message.room == room)\
        .order_by(models.Message.created_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()
    return messages

@app.post("/messages", response_model=schemas.MessageResponse)
async def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_message = models.Message(
        sender=message.sender,
        message=message.message,
        room=message.room
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Serialize to schema
    response_msg = schemas.MessageResponse.model_validate(db_message)
    # Broadcast to websocket clients in the room
    await manager.broadcast(response_msg.model_dump(mode="json"), db_message.room)
    
    return db_message

@app.delete("/messages/{id}")
async def delete_message(id: int, db: Session = Depends(get_db)):
    db_message = db.query(models.Message).filter(models.Message.id == id).first()
    if not db_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    room = db_message.room
    db.delete(db_message)
    db.commit()
    
    # Broadcast deletion event so frontend removes it from DOM
    deletion_event = {"event": "delete", "message_id": id}
    await manager.broadcast(deletion_event, room)
    
    return {"message": "Deleted"}

# WebSocket Endpoint
@app.websocket("/ws/{room}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room: str, client_id: str):
    await manager.connect(websocket, room)
    db = SessionLocal()
    try:
        while True:
            # Expect client to send JSON: {"sender": "...", "message": "..."}
            data = await websocket.receive_json()
            sender = data.get("sender", "Guest")
            message_text = data.get("message", "")
            
            if not message_text.strip():
                continue
                
            db_message = models.Message(
                sender=sender,
                message=message_text,
                room=room
            )
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            
            response_msg = schemas.MessageResponse.model_validate(db_message)
            await manager.broadcast(response_msg.model_dump(mode="json"), room)

            # Smart Auto-Reply Bot
            if sender.lower() != "chatbot":
                # Wait 1 second to make the response feel natural
                await asyncio.sleep(1.0)
                
                msg_lower = message_text.lower()
                if room == "tech":
                    bot_text = f"Hey {sender}, interesting tech topic! Have you looked at the official documentation or GitHub for solutions?"
                elif room == "ideas":
                    bot_text = f"That's a creative idea, {sender}! We should brainstorm this further during our next team sync."
                elif "hello" in msg_lower or "hi" in msg_lower:
                    bot_text = f"Hello {sender}! Welcome to #{room}. How can I assist you today?"
                elif "help" in msg_lower:
                    bot_text = f"Hi {sender}, I can help you! You can switch chat rooms on the left sidebar to explore different discussions."
                else:
                    bot_text = f"Thanks for sharing that in #{room}, {sender}! 👍"
                
                db_bot_message = models.Message(
                    sender="ChatBot",
                    message=bot_text,
                    room=room
                )
                db.add(db_bot_message)
                db.commit()
                db.refresh(db_bot_message)
                
                bot_response = schemas.MessageResponse.model_validate(db_bot_message)
                await manager.broadcast(bot_response.model_dump(mode="json"), room)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
    except Exception as e:
        print(f"WebSocket Error: {e}")
        manager.disconnect(websocket, room)
    finally:
        db.close()