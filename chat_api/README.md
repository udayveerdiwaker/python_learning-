# 💬 Advanced Realtime Chat API & client

An advanced, production-ready real-time multi-room chat application featuring a high-performance **FastAPI** backend with **SQLAlchemy/SQLite** persistence and a premium, responsive glassmorphic dark-mode web client.

---

## ✨ Features

1. **Real-time WebSockets**: Instant message delivery and synchronized deletions across all connected clients in a specific room.
2. **Multi-Room Architecture**: Join different rooms (`#general`, `#tech`, `#ideas`, `#random`) with separate message isolation.
3. **Database Persistence**: Messages are persisted locally in a SQLite database (`chat.db`) using SQLAlchemy ORM.
4. **Frosted-Glass UI**: A premium dark-mode, glassmorphic UI served directly from the root path (`/`) with a connection status indicator, customizable nicknames, and delete options.
5. **Dual REST/WS API**: Send messages either in real-time over WebSockets or through standard REST JSON payloads.

---

## 🛠️ Project Structure

```text
chat_api/
├── templates/
│   └── index.html      # Glassmorphic Frontend Client
├── database.py         # SQLAlchemy connection & session dependency
├── main.py             # FastAPI App, WebSockets manager & REST routes
├── models.py           # SQLAlchemy Database Model (Message table)
├── schemas.py          # Pydantic schemas (validation/serialization)
├── requirements.txt    # Python dependencies
├── README.md           # Setup and API documentation
└── chat.db             # Local SQLite database (created on startup)
```

---

## 🚀 Getting Started

### 1. Installation

Set up your environment and install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Initialize Database (Optional)

The application automatically creates the database on startup. However, you can also pre-create/initialize the database tables by running the helper script:

```bash
python create_db.py
```

### 3. Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

* **Web Client / UI**: Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser. Open multiple tabs to test real-time chat sync!
* **Swagger API Docs**: Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore/test REST endpoints interactively.

---

## 🔌 API Reference

### 1. REST Endpoints

#### GET `/messages`
* **Description**: Retrieve message history for a specific room.
* **Query Parameters**:
  * `room` (string, default: `general`)
  * `limit` (integer, default: `50`)
  * `offset` (integer, default: `0`)
* **Response**:
  ```json
  [
    {
      "id": 1,
      "sender": "Alice",
      "message": "Hey everyone!",
      "room": "general",
      "created_at": "2026-06-24T12:00:00"
    }
  ]
  ```

#### POST `/messages`
* **Description**: Send a new message (persists to DB and broadcasts to WebSocket clients).
* **Request Body**:
  ```json
  {
    "sender": "Alice",
    "message": "Hello!",
    "room": "general"
  }
  ```

#### DELETE `/messages/{id}`
* **Description**: Delete a message by ID (removes from DB and broadcasts deletion event to WebSockets).
* **Response**:
  ```json
  {
    "message": "Deleted"
  }
  ```

---

### 2. WebSocket Protocol

* **Endpoint URL**: `ws://127.0.0.1:8000/ws/{room_name}/{client_id}`
* **Client Message Payload**:
  ```json
  {
    "sender": "Alice",
    "message": "Hello via WS!"
  }
  ```
* **Server Broadcast Payload** (sent to all clients in the room):
  ```json
  {
    "id": 2,
    "sender": "Alice",
    "message": "Hello via WS!",
    "room": "general",
    "created_at": "2026-06-24T12:05:00"
  }
  ```
* **Server Deletion Broadcast**:
  ```json
  {
    "event": "delete",
    "message_id": 2
  }
  ```
