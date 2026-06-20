# Module 10: Interactive AI Coding Assistant App 🤖

Welcome to the capstone project of the Python Practice Curriculum! In this module, you will build and launch a premium, full-stack **AI Coding Assistant Web Application**.

---

## 🎨 Design & Features

- **Premium Interface**: A modern, dark-themed, glassmorphic chat dashboard.
- **Micro-Animations**: Hover effects, fade-in chat bubbles, and an animated AI typing indicator.
- **FastAPI Backend**: Serves the single-page application (SPA) and exposes the `/api/chat` streaming or standard JSON completion routes.
- **Gemini API Integration**: Uses Google's Gemini models to respond to coding questions.
- **Graceful Fallback**: If no `GEMINI_API_KEY` is detected in the environment variables, the backend automatically falls back to a smart, simulated local AI mode so the app remains fully functional!

---

## 🚀 Running the Application

1. Open your terminal in this folder:
   ```bash
   cd python_practice/10_ai_coding_assistant
   ```
2. (Optional) Set your Gemini API Key in your terminal session:
   - **PowerShell (Windows)**:
     ```powershell
     $env:GEMINI_API_KEY="your_api_key_here"
     ```
   - **Command Prompt (Windows)**:
     ```cmd
     set GEMINI_API_KEY=your_api_key_here
     ```
   - **Linux / macOS**:
     ```bash
     export GEMINI_API_KEY="your_api_key_here"
     ```
3. Start the application:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. Open your browser and navigate to: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📁 Project Structure

- `main.py`: The FastAPI server serving HTML/CSS/JS and routing user prompts to Gemini or the fallback generator.
- `templates/index.html`: The HTML layout for the assistant dashboard.
- `static/styles.css`: Glassmorphic, dark-mode CSS styling.
- `static/app.js`: JavaScript handling input submissions, loading states, and chat element creation.
