# Smart Task Analyzer (Minimal Submission)

This is a minimal, self-contained implementation of the **Smart Task Analyzer** assignment.
It contains a Django backend (minimal setup), a simple scoring algorithm, API endpoints, a basic frontend, unit tests, and example results.

**Files included:** see project structure below.

**Reference:** Assignment PDF included by the user. fileciteturn0file0

## How to run (quick)
1. Create & activate venv (Python 3.8+)
2. Install requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Run server: `python manage.py runserver`
5. Open `frontend/index.html` in browser for a simple frontend that posts to the API.

(If serving frontend from Django, copy files into a static folder or use a simple file server.)

## What I implemented (high level)
- Django project `backend/` with app `tasks`
- `tasks/scoring.py`: scoring algorithm (urgency, importance, effort, dependencies)
- API endpoints:
  - POST `/api/tasks/analyze/` - returns tasks with `score`
  - GET `/api/tasks/suggest/` - top 3 tasks with explanation
- Frontend `frontend/index.html` to paste JSON or add tasks and call the API
- Unit tests for scoring algorithm (`tasks/tests.py`)
- Sample `sample_input.json` and `sample_results.json`

## Notes / Trade-offs
- This is a minimal local implementation aimed to satisfy the assignment requirements quickly.
- The Django settings are simplified for local development and use SQLite.
- Circular dependency detection is handled with a simple DFS guard in scoring.
- Edge cases (missing fields, invalid dates) are handled with defaults and validation.

