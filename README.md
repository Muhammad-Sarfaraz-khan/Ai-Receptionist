

#  AI Receptionist System

An AI-powered receptionist application designed for IT Service Agencies (and extendable to restaurants), featuring a modern React frontend and a FastAPI backend. The system is built to automate lead handling, basic customer interaction, and service workflows.

---

## 📌 Project Overview

The AI Receptionist acts as a virtual front desk that can:

* Greet users
* Collect lead information
* Connect to backend services
* Be extended with AI, Google Sheets, and Email integrations

This project follows **best-practice frontend–backend separation** and is scalable for real-world usage.

---

## 🧱 Tech Stack

### 🔹 Frontend

* **React.js** (Vite)
* JavaScript (JSX)
* CSS (Global styling)
* Fetch API (for backend communication)

### 🔹 Backend

* **Python**
* **FastAPI**
* Uvicorn (ASGI server)
* CORS Middleware

### 🔹 Future Integrations (Planned)

* OpenAI / LLM APIs
* Google Sheets API (Lead storage)
* Email Service (SendGrid / SMTP)
* Database (PostgreSQL / SQLite)

---

## 📁 Project Structure

```
ai_receptionist/
│
├── backend/
│   ├── main.py
│   ├── ai_service.py
│   ├── appointments.py
│   └── acts.py
│
├── frontend/
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── Header.jsx
│   │   │   └── Message.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── styles/
│   │       └── global.css
│
└── README.md
```

---

## ▶️ How to Run the Project

### ✅ Backend Setup

```bash
cd backend
pip install fastapi uvicorn
uvicorn main:app --reload
```

Backend will run at:

```
http://127.0.0.1:8000
```

---

### ✅ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at:

```
http://localhost:5173
```

---

## 🔄 Application Flow

1. User opens the frontend (React app)
2. `main.jsx` loads the `App` component
3. `App.jsx` renders the `Home` page
4. Frontend can send requests to FastAPI backend
5. Backend processes requests and responds with data
6. (Future) AI model handles conversation logic

---

## 🧠 Key Concepts Used

* Component-based UI architecture
* Separation of concerns (Frontend vs Backend)
* REST API communication
* Scalable project structure
* Ready for AI & automation integration

---



