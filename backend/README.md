# Backend – Trivia API (Flask)

A lightweight Flask + SQLAlchemy backend for the Trivia game. It serves categories, questions (with pagination), search, deletion, and quiz play.

---

## Requirements

- Python **3.10+**
- PostgreSQL **12+**
- `pip`, `virtualenv` (recommended)

---

## Quick Start

### 1) Environment

From the `backend/` folder, create and activate a virtual environment:

- Linux/macOS: `python3 -m venv env && source env/bin/activate`
- Windows (PowerShell): `py -m venv env; .\env\Scripts\Activate.ps1`

Install dependencies:

- `pip install -r requirements.txt`

Set environment variables (use a `.env` in `backend/` or export them in your shell):

- `DATABASE_URL` (dev DB, e.g. `postgresql://postgres:postgres@127.0.0.1:5432/trivia`)
- `DATABASE_URL_TEST` (test DB, e.g. `postgresql://postgres:postgres@127.0.0.1:5432/trivia_test`)

> Tip: Don’t commit secrets. `.env` is supported via **python-dotenv** and Flask.

### 2) Databases

Create and seed databases (adjust user/host as needed):

- Create dev DB: `createdb trivia`
- Create test DB: `createdb trivia_test`
- Seed dev DB (optional): from `backend/`, run `psql trivia < trivia.psql`

### 3) Run the Dev Server (from `backend/`)

- Linux/macOS: `FLASK_APP=flaskr flask run`
- Windows (PowerShell): `$env:FLASK_APP="flaskr"; flask run`

API base: **http://127.0.0.1:5000**

---

## API Overview

All responses are JSON. CORS is enabled for `*`. Pagination size: **10**.

### `GET /categories`
Returns a map of category IDs to names.

Response:
- `{ "success": true, "categories": { "1": "Science", ... } }`

### `GET /questions?page={number}`
Returns paginated questions, total count, categories, and current category (null).

Response fields:
- `questions`: array of `{ id, question, answer, difficulty, category }`
- `total_questions`: integer
- `categories`: same map as `/categories`
- `current_category`: null
- `success`: true

### `GET /categories/{id}/questions`
Returns all questions in a category.

Response fields:
- `questions`: array
- `total_questions`: integer
- `current_category`: category name
- `success`: true

### `DELETE /questions/{id}`
Deletes a question by ID.

Response:
- `{ "success": true, "deleted": id }`

### `POST /questions` (create)
Create a new question.

Body:
- `{ "question": str, "answer": str, "difficulty": int, "category": int }`

Response:
- `{ "success": true, "created": id }` (HTTP 201)

### `POST /questions` (search)
Search for questions by substring.

Body:
- `{ "searchTerm": str }`

Response:
- `{ "success": true, "questions": [...], "total_questions": n, "current_category": null }`

### `POST /quizzes`
Return a random next question not in `previous_questions`.

Body:
- `{ "previous_questions": [ids], "quiz_category": { "id": number | 0, "type": "click" | name } }`

Response:
- `{ "success": true, "question": { ... } | null }`

---

## Error Handling

Errors return JSON with `success: false`, an error code, and a message.

- **400**: `{ "success": false, "error": 400, "message": "bad request" }`
- **404**: `{ "success": false, "error": 404, "message": "resource not found" }`
- **422**: `{ "success": false, "error": 422, "message": "unprocessable" }`
- **500**: `{ "success": false, "error": 500, "message": "internal server error" }`

---

## Testing

- Ensure `DATABASE_URL_TEST` points to your test DB (e.g. `trivia_test`).
- (Optional) Seed test DB if needed: `psql trivia_test < trivia.psql`
- From `backend/`, run: `python -m unittest test_flaskr.py`
- Tests will reset the schema and seed minimal data automatically.

---

## Notes

- **Env-first config**: the app reads `DATABASE_URL` and `DATABASE_URL_TEST`.
- Keep secrets out of version control.
- If you change endpoint shapes, update the frontend accordingly (`frontend/`).
