# Frontend – Trivia UI (React)

A React SPA for the Trivia game. It talks to the Flask backend to fetch categories, list/paginate questions, search, and play quizzes.

---

## Requirements

- Node.js **16.x**
- npm

---

## Setup

1. Install dependencies: `npm install`
2. Start dev server: `npm start`
3. Open **http://localhost:3000**

> The app assumes the backend API is running at **http://127.0.0.1:5000**.

---

## API Base URL

### Option A: Default (no action)
- The UI calls `http://127.0.0.1:5000` by default (where the Flask API runs).

### Option B: Environment variable (recommended)
1. Create a `.env` file in `frontend/` with:
   - `REACT_APP_API_BASE=http://127.0.0.1:5000`
2. Restart `npm start` after changing env.

### Option C: Modify code
- Update the API base in your fetch/axios config (e.g., `src/config.js` or `src/api/*.js`).

---

## Scripts

- `npm start` – run the dev server (Fast Refresh enabled)
- `npm run build` – production build to `build/`
- `npm test` – run unit tests (if configured)
- `npm run lint` – lint the project (if configured)

---

## Expected Backend Endpoints (Summary)

- `GET /categories` → `{ success, categories }`
- `GET /questions?page=n` → `{ success, questions, total_questions, categories, current_category }`
- `GET /categories/{id}/questions` → `{ success, questions, total_questions, current_category }`
- `DELETE /questions/{id}` → `{ success, deleted }`
- `POST /questions` (create) → `{ success, created }`
- `POST /questions` (search) → `{ success, questions, total_questions, current_category }`
- `POST /quizzes` → `{ success, question | null }`

> If you change response shapes, make corresponding adjustments in the frontend.

---

## Styling / Customization

- Components live in `src/components/`.
- Add styles via CSS/SCSS/CSS-in-JS as you prefer.
- Feel free to extend gameplay mechanics (e.g., number of questions, scoring). Document changes in the root README.

---

## Troubleshooting

- 404/500 errors: verify the backend is running and CORS is enabled.
- Empty lists: ensure the DB is seeded and the backend is pointing at the correct database.