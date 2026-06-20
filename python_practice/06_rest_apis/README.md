# Module 06: REST APIs 🌐

In this module, you will learn the core architectural principles of **REST (Representational State Transfer)**, which is the standard design pattern used to build clean, maintainable web APIs.

---

## 📚 REST Core Principles

1. **Client-Server Architecture**: The frontend (client) and backend (server) are separate. They only communicate via HTTP requests and responses.
2. **Stateless**: Every request from a client must contain all the information needed to understand and process it. The server does not store session memory about the client on its side.
3. **Uniform Interface**: Resources are identified by URIs (Uniform Resource Identifiers). Standard HTTP methods are used to manipulate these resources.

---

## 🚦 HTTP Methods (Verbs)

REST API endpoints represent **nouns** (resources) and use **verbs** (HTTP methods) to execute actions:

| HTTP Verb | CRUD Action | URI Example | Description |
| :--- | :--- | :--- | :--- |
| **`GET`** | Read | `/posts` | Retrieves all posts |
| **`GET`** | Read | `/posts/45` | Retrieves post with ID 45 |
| **`POST`** | Create | `/posts` | Creates a new post (data in Request Body) |
| **`PUT`** | Update (Full) | `/posts/45` | Replaces post 45 completely |
| **`PATCH`** | Update (Partial) | `/posts/45` | Modifies specific fields of post 45 |
| **`DELETE`**| Delete | `/posts/45` | Deletes post 45 |

---

## 🔢 Common HTTP Status Codes

Your API should return the correct status code so clients know what happened:
- **`200 OK`**: Request succeeded.
- **`201 Created`**: POST request succeeded, resource created.
- **`400 Bad Request`**: Server cannot process the request due to client error (e.g. malformed JSON).
- **`401 Unauthorized`**: Authentication is required or has failed.
- **`403 Forbidden`**: Client is authenticated but does not have permission for the resource.
- **`404 Not Found`**: The requested resource does not exist.
- **`500 Internal Server Error`**: Something went wrong on the server's side.

---

## 🗂️ Files in this Module

- `api_crud.py`: A REST API server implementing all standard REST endpoints for managing a list of `tasks` (in-memory) with correct verbs, path variables, and status codes. Run it using:
  ```bash
  uvicorn api_crud:app --reload --port 8000
  ```
- `exercises.md`: A markdown file containing quiz questions and exercises on designing RESTful resource paths.
- `challenge.md`: A design challenge requiring you to implement a REST API for a **Movie Rental System**.
