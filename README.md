# Photo Feed & Analytics Dashboard

A modern, high-performance web application featuring a secure **FastAPI** backend and a glassmorphic **React + Vite** frontend.

---

## 🚀 How to Run the Project

Follow these steps to run the application locally on your computer:

### 1. Start the Backend (FastAPI)
1. Open a terminal window.
2. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   python main.py

   python -m uvicorn main:app --reload
   ```
   *The backend server will run at: **`http://127.0.0.1:8000`***

---

### 2. Start the Frontend (React + Vite)
1. Open a **new/second** terminal window.
2. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
3. Install the node packages:
   ```bash
   npm install
   ```
4. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend dashboard will run at: **`http://localhost:5173`***

---

## 🛠️ Project Structure
```text
python_learning-/
├── backend/
│   ├── main.py          # FastAPI application server & routes
│   ├── posts.json       # Local JSON database (holds 10,000 seeded posts)
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main frontend router & tabs manager
│   │   ├── index.css    # Premium CSS design tokens & animations
│   │   └── components/  # Reusable React components
│   ├── package.json     # Node scripts & packages dependencies
│   └── vite.config.js   # Vite configuration with proxy rules
└── README.md            # Setup and running instructions
```

## ✨ Key Features
- **Smart Numbered Pagination**: Batches 10,000 seeded posts in sections of 12 items for optimal page speed.
- **Glassmorphism Design**: Sleek dark mode visual interface with smooth micro-animations.
- **Bearer Token Security**: Generate secure api keys and authenticate requests to create or like posts.
- **Search & Filters**: Instantly query titles, descriptions, and authors or filter posts by category tags.
