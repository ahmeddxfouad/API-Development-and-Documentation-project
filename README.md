# Trivia API – Full Stack Project

A full-stack Trivia game with a **Flask + SQLAlchemy** backend and a **React** frontend. The backend exposes REST endpoints for categories, questions (CRUD + search), and quiz play. The frontend consumes these APIs and provides the game UX.

---

## R    epo Layout

- **backend/** – Flask application (API, models, tests)
- **frontend/** – React application (UI)
- **README.md** – You are here

---

## Prerequisites

- Python **3.10+**
- PostgreSQL **12+**
- Node.js **16.x** and npm
- (Recommended) `virtualenv` for Python

---

## Quick Start (Dev)

### 1) Backend (start first)

1. Create and activate a virtual environment (from `backend/`).
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment:
   - `DATABASE_URL` (e.g., `postgresql://postgres:postgres@127.0.0.1:5432/trivia`)
   - `DATABASE_URL_TEST` (e.g., `postgresql://postgres:postgres@127.0.0.1:5432/trivia_test`)
   - You can place them in `backend/.env` (python-dotenv is supported).
4. Create databases:
   - `createdb trivia`
   - `createdb trivia_test`
   - Seed dev DB (optional): from `backend/` run `psql trivia < trivia.psql`
5. Run server:
   - Linux/macOS: `FLASK_APP=flaskr flask run`
   - Windows (PowerShell): `$env:FLASK_APP="flaskr"; flask run`
6. API runs at: **http://127.0.0.1:5000**

### 2) Frontend

1. From `frontend/` install dependencies: `npm install`
2. (Optional) Configure API base URL:
   - Default assumes backend at `http://127.0.0.1:5000`
   - To override, create `frontend/.env` with: `REACT_APP_API_BASE=http://your-api:5000`
3. Start dev server: `npm start`
4. App runs at: **http://127.0.0.1:3000**

---

## Testing

### Backend
- Ensure `DATABASE_URL_TEST` points to your test DB.
- Run from `backend/`: `python -m unittest test_flaskr.py`

### Frontend
- If tests are configured: `npm test` (from `frontend/`).

---

## Deployment Notes

- Keep secrets in environment variables; **do not commit** passwords.
- If you change backend endpoint shapes, update the frontend API calls.
- CORS is enabled in the backend for local development.

---

## Troubleshooting

- **Cannot connect to DB**: verify `DATABASE_URL`, DB is running, and user permissions.
- **Frontend cannot load categories/questions**: ensure backend is running on `http://127.0.0.1:5000` or update `REACT_APP_API_BASE`.
- **Tests fail with schema errors**: drop/recreate test DB and re-run.

---

## License

See `LICENSE.txt`.