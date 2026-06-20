# main.py
import os
import sys
from pathlib import Path

# Add project root to sys path
sys.path.append(str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Try to import Google Generative AI package
try:
    import google.generativeai as genai
    HAS_GEMINI_LIB = True
except ImportError:
    HAS_GEMINI_LIB = False

app = FastAPI(
    title="AI Coding Assistant Capstone",
    description="Interactive chat interface powered by Gemini.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# 1. API Configuration & Key Validation
# ------------------------------------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
IS_LIVE_MODE = False

if HAS_GEMINI_LIB and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        IS_LIVE_MODE = True
        print("🚀 Gemini API successfully configured. Live Assistant is active!")
    except Exception as e:
        print(f"⚠️ Error configuring Gemini: {e}. Falling back to Simulated Assistant.")
else:
    print("ℹ️ GEMINI_API_KEY not found in environment. Running in Simulated Local Assistant mode.")


# ------------------------------------------------------------------------------
# 2. Schemas & Static Mounting
# ------------------------------------------------------------------------------
class ChatPrompt(BaseModel):
    message: str

# Create directories if they do not exist
current_dir = Path(__file__).resolve().parent
(current_dir / "static").mkdir(exist_ok=True)
(current_dir / "templates").mkdir(exist_ok=True)

# Mount the static folder at /static
app.mount("/static", StaticFiles(directory=str(current_dir / "static")), name="static")


# ------------------------------------------------------------------------------
# 3. HTTP Route Handlers
# ------------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse, tags=["UI"])
def serve_index_page():
    """
    Renders and serves the single-page application dashboard.
    """
    html_path = current_dir / "templates" / "index.html"
    if not html_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="index.html template missing."
        )
    return html_path.read_text(encoding="utf-8")


@app.post("/api/chat", tags=["AI API"])
def handle_chat_completion(prompt: ChatPrompt):
    """
    Accepts user prompts, routes them to Gemini (if active), or supplies
    pre-configured smart replies.
    """
    user_input = prompt.message.strip()
    if not user_input:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty."
        )
        
    if IS_LIVE_MODE:
        try:
            # Query Gemini model
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"You are a helpful Python and FastAPI coding tutor. "
                f"Answer the user's question clearly. Question: {user_input}"
            )
            return {"reply": response.text, "mode": "Live (Gemini API)"}
        except Exception as e:
            return {
                "reply": f"Error calling Gemini: {str(e)}. Falling back to offline template.",
                "mode": "Error Fallback"
            }
            
    # Graceful Offline Mock Replies
    reply = get_simulated_ai_response(user_input)
    return {"reply": reply, "mode": "Local Sim (Set GEMINI_API_KEY for live mode)"}


# ------------------------------------------------------------------------------
# 4. Local AI Response Generator
# ------------------------------------------------------------------------------
def get_simulated_ai_response(prompt: str) -> str:
    """
    Simulates a coding assistant reply based on keywords.
    """
    p = prompt.lower()
    if "fastapi" in p:
        return (
            "### FastAPI Basics 🚀\n\n"
            "FastAPI is a modern, high-performance web framework for building APIs with Python.\n"
            "Here is how you start a minimal server:\n\n"
            "```python\n"
            "from fastapi import FastAPI\n\n"
            "app = FastAPI()\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'hello': 'world'}\n"
            "```\n\n"
            "Run it with: `uvicorn main:app --reload`"
        )
    elif "mysql" in p or "db" in p:
        return (
            "### Connecting to MySQL in Python 🐬\n\n"
            "To connect to MySQL, you can use `mysql-connector-python` or SQLAlchemy ORM.\n"
            "Make sure your local XAMPP/MySQL database server is running, then write:\n\n"
            "```python\n"
            "import mysql.connector\n\n"
            "conn = mysql.connector.connect(\n"
            "    host='localhost',\n"
            "    user='root',\n"
            "    password='',\n"
            "    database='python_practice_db'\n"
            ")\n"
            "```"
        )
    elif "jwt" in p or "token" in p or "auth" in p:
        return (
            "### JWT Authentication Security 🔒\n\n"
            "JSON Web Tokens (JWT) are signed cryptographically. "
            "In FastAPI, you protect endpoints by depending on the token parsing utility:\n\n"
            "```python\n"
            "from fastapi.security import OAuth2PasswordBearer\n"
            "from fastapi import Depends\n\n"
            "oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')\n\n"
            "@app.get('/secure-route')\n"
            "def secure(token: str = Depends(oauth2_scheme)):\n"
            "    return {'status': 'authorized'}\n"
            "```"
        )
    else:
        return (
            "Hello! I am your **Python Curriculum Assistant**.\n\n"
            "I detected your query. To enable live AI generation: \n"
            "1. Close the server.\n"
            "2. Set the `GEMINI_API_KEY` environment variable: `set GEMINI_API_KEY=your_key`.\n"
            "3. Restart the server: `uvicorn main:app --reload`.\n\n"
            "Let me know if you want to know about **FastAPI**, **MySQL Connection**, or **JWT Auth**!"
        )

# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
