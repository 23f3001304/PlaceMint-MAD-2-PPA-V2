# PlaceMint - Placement Portal Application (PPA)

A campus recruitment portal for an institute's placement cell. It replaces the
usual spreadsheet-and-email workflow with one system where the placement cell
(Admin), Companies, and Students each work from their own dashboard: companies
get approved and post drives, students apply and track status, and the admin
moderates everything and watches the numbers.

Built for the MAD-II project brief on a fixed stack: Flask API, Vue 3 SPA,
Bootstrap 5, SQLite, Redis, and Celery.

## What each role can do

**Admin** (seeded once, no registration)
- Dashboard with institute-wide counts and Chart.js analytics
- Approve or reject company registrations and placement drives
- Search companies and students; blacklist or deactivate accounts; remove records
- View every application; mark drives complete

**Company** (self-registers, then waits for admin approval)
- Dashboard with drive, applicant, shortlist and placement counts
- Post drives (drive name, role, description, eligibility, skills, salary, deadline)
- Review applicants: shortlist, schedule interviews, extend offers, record hires
- Open/close drives; export applicant history as CSV; edit the company profile

**Student** (self-registers)
- Profile with branch, CGPA, skills, resume upload
- Browse organizations and drives they are eligible for; search and filter
- Apply once per drive (duplicate, eligibility and deadline guards enforced)
- Track application status, interviews and feedback; download offer letters
- Export application history as CSV

**Extras:** pre-login public landing page with live aggregate stats, an ATS-style
resume screener, an installable PWA, daily reminder and monthly report jobs.

## Tech stack

| Layer    | Choice                                            |
|----------|---------------------------------------------------|
| API      | Flask + Flask-SQLAlchemy                          |
| Auth     | JWT (Flask-JWT-Extended), role-based access       |
| Database | SQLite (schema created programmatically)          |
| Cache    | Redis via Flask-Caching (read-through + expiry)   |
| Jobs     | Celery + Celery Beat on Redis                     |
| Frontend | Vue 3 single-file components (Vite)               |
| Styling  | Bootstrap 5 + a small custom theme                |
| Charts   | Chart.js                                          |

Two conventions hold throughout: no source file exceeds 200 lines, and no folder
holds more than four source files before it splits into subfolders.

## Project layout

```
backend/
  app/
    api/         REST blueprints (auth, admin, company, student, documents, exports)
    auth/        password hashing, JWT wiring, RBAC decorator
    caching/     Redis cache keys + read-through helpers
    models/      SQLAlchemy models (user, profiles, placement, export job)
    services/    business logic (accounts, drives, applications, stats, exports)
    tasks/       Celery jobs (reminders, reports, exports)
    utils/       responses, validation, email, errors
  tests/         unittest suite (auth, rules, jobs, caching)
  run.py         dev server        celery_worker.py   Celery entry
  seed_demo.py   demo data         requirements.txt   .env.example
frontend/
  src/
    api/         fetch client + endpoint modules
    components/  ui, layout, forms, overlays, charts, media
    composables/ useAsync, useExport
    router/      routes, guards, nav
    store/       reactive auth + toast stores
    views/       auth, admin, company, student, landing, ATS
    styles/      Bootstrap theme (SCSS) + custom layer
```

## ER Diagram

The database schema used by the app is documented in  [docs/sqlite (1).png](docs/sqlite%20(1).png).

## Getting started

### Prerequisites
- Python 3.11+
- Node 18+ and npm
- Redis. Easiest cross-platform is Docker (used by the launcher script below):
  `docker run -d --name ppa-redis -p 6379:6379 redis:alpine` (restart later with
  `docker start ppa-redis`). On Windows without Docker, **Memurai** is a native
  drop-in (`winget install Memurai.MemuraiDeveloper`); WSL (`sudo apt install
  redis-server`) also works.

### 1. Backend API
```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows;  source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
copy .env.example .env           # optional; sensible defaults work out of the box
python run.py                    # http://127.0.0.1:5000
```
The SQLite database and the admin account are created automatically on first run.

Load demo data (three companies, five students, four drives, applications and a
placement) with:
```bash
python seed_demo.py
```

### 2. Frontend SPA
```bash
cd frontend
npm install
npm run dev                      # http://127.0.0.1:5173, proxies /api to Flask
```
For a production-style run, `npm run build` outputs to `frontend/dist`, which
Flask can serve as static files.

### 3. Background jobs (Celery + Redis)
With Redis running, start the worker and the scheduler. On **Windows** they must
be separate processes (`--pool=solo` is required, and embedded `-B` beat is not
supported there):
```bash
cd backend && venv\Scripts\activate
celery -A celery_worker.celery worker --pool=solo --loglevel=info   # terminal A
celery -A celery_worker.celery beat --loglevel=info                 # terminal B
```
On macOS/Linux you can combine them into one: `celery -A celery_worker.celery worker -B`.
The daily reminder (08:00 UTC) and monthly report (1st of the month) fire on
schedule; the user-triggered CSV export runs as soon as a student or company
requests it.

To demo exports without a worker, run the API with `CELERY_TASK_ALWAYS_EAGER=1`
so jobs run inline (this is also how the test suite runs). The default is real
Celery + Redis.

### Run the whole stack at once (Windows)
Once the venv, `npm install`, and Docker are ready, one command opens Redis, the
API, the Celery worker and beat, and the Vite dev server, each in its own window:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1
```

## Demo accounts

After `seed_demo.py` (all demo passwords are `password123`):

| Role    | Email             | Password    |
|---------|-------------------|-------------|
| Admin   | coehemang@gmail.com | admin123  |
| Company | tech@demo.com     | password123 |
| Student | ada@demo.com      | password123 |

## Running the tests

```bash
cd backend
python -m unittest discover -s tests
```
The suite (auth, placement rules, background jobs, caching) uses an in-memory
database and runs Celery eagerly, so it needs neither Redis nor a worker.

## Security

- Passwords hashed with Werkzeug (PBKDF2). JWT auth carries a role claim, checked
  on every protected route together with the account's active/blacklist status.
- Rate limiting on login, registration and export (Redis-backed, with an
  in-process fallback; fails open if neither is reachable so auth stays available).
- Security headers on every response: `X-Content-Type-Options: nosniff`,
  `X-Frame-Options: DENY`, `Referrer-Policy`, and a Content-Security-Policy.
- Generated offer letters and report emails HTML-escape user data; CSV exports
  neutralise spreadsheet formula-injection; SQLAlchemy parameterises all queries;
  resume/offer-letter/export access is owner-and-role gated.
- Set strong `SECRET_KEY` and `JWT_SECRET_KEY` in `.env` before any real deploy;
  the defaults are development placeholders only.

## Notes
- Email uses a console backend by default (messages are logged), so reminders and
  reports work with no mail server. Set `MAIL_BACKEND=smtp` plus the `SMTP_*`
  values in `.env` to send real mail.
- Caching degrades gracefully: if Redis is down the API computes directly instead
  of erroring, so the app still runs (uncached).
- Only the mandated frameworks are used, plus Vue Router, Chart.js (allowed for
  charts) and the standard Flask companions (SQLAlchemy, JWT, Caching).
