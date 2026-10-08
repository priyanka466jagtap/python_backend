# Run the project

Backend code is in `backend/`; React frontend code is in `frontend/`.

## Backend

From the project root in PowerShell:

```powershell
.\backend\myenv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000
```

Keep the existing PostgreSQL database running on `localhost:5432` with
the connection configured in `backend/database.py`.

Alternatively, run from inside the backend folder:

```powershell
cd backend
.\myenv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

## Frontend

In another terminal, from the project root:

```powershell
cd frontend
npm start
```

The frontend runs on `http://localhost:3000` and connects to the backend
on `http://localhost:8000`.

## Setup after cloning

From the project root:

```powershell
python -m venv backend/myenv
.\backend\myenv\Scripts\python.exe -m pip install -r backend/requirements.txt
cd frontend
npm install
```

Virtual environments, Python caches and frontend dependencies are ignored by Git.
