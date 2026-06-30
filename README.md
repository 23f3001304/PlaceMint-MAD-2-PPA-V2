# Placement Portal Application (PPA)

A campus recruitment portal for an institute's placement cell. It replaces the
usual spreadsheet-and-email workflow with a single system where the placement
cell (Admin), Companies, and Students each work from their own dashboard:
companies get approved and post drives, students apply and track status, and the
admin moderates everything and watches the numbers.

Built for the MAD-II project brief. Stack is fixed by the brief: Flask API, Vue 3
SPA, Bootstrap 5, SQLite, Redis, and Celery.

## Roles at a glance

- **Admin** (placement cell) is seeded once at startup and cannot be registered.
  Approves/removes companies and drives, searches and blacklists users, and sees
  institute-wide statistics.
- **Company** self-registers, then waits for admin approval before it can post
  job drives, review applicants, shortlist, schedule interviews, and record hires.
- **Student** self-registers, completes a profile (branch, CGPA, skills, resume),
  browses drives they are eligible for, applies once per drive, and tracks each
  application through the pipeline.

## Tech stack

| Layer      | Choice                                        |
|------------|-----------------------------------------------|
| API        | Flask + Flask-SQLAlchemy                      |
| Auth       | JWT (Flask-JWT-Extended), role-based          |
| Database   | SQLite (schema created programmatically)      |
| Cache      | Redis via Flask-Caching                       |
| Jobs       | Celery + Celery Beat on Redis                 |
| Frontend   | Vue 3 (Vite single-file components)           |
| Styling    | Bootstrap 5 + a small custom theme            |
| Charts     | Chart.js                                       |

The visual theme (cream base, forest-green accent, editorial type) is a custom
Bootstrap layer, not a second CSS framework.

## Project layout

```
backend/    Flask application (app factory, models, API blueprints, services, tasks)
frontend/   Vue 3 + Vite single-page app (views, components, api client, theme)
```

Two conventions hold throughout the codebase: no source file exceeds 200 lines,
and no folder holds more than four source files before it splits into subfolders.

## Getting started

### Prerequisites

- Python 3.11+
- Node 18+ and npm
- Redis. On Windows the simplest option is **Memurai** (a native Redis for
  Windows): `winget install Memurai.MemuraiDeveloper`. WSL (`sudo apt install
  redis-server`) or Docker (`docker run -p 6379:6379 redis`) also work.

### 1. Backend API

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows;  source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
copy .env.example .env           # then edit if needed
python run.py                    # serves http://127.0.0.1:5000
```

The database file and the admin account are created automatically on first run.
Default admin login is `admin@ppa.local` / `admin123` (change via `.env`).

### 2. Frontend SPA

```bash
cd frontend
npm install
npm run dev                      # serves http://127.0.0.1:5173, proxies /api to Flask
```

For a production-style demo, `npm run build` outputs to `frontend/dist`, which
Flask serves directly.

### 3. Background jobs (Celery)

With Redis running, in two more terminals:

```bash
cd backend
venv\Scripts\activate
celery -A celery_worker.celery worker --pool=solo -B --loglevel=info
```

`--pool=solo` is required on Windows; `-B` runs the beat scheduler in the same
process so the daily reminder and monthly report jobs fire on schedule.

## License

Coursework project. Not licensed for redistribution.
