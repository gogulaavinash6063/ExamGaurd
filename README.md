# ExamGuard — Milestone 1 & 2 completion

This package finishes and fixes everything up through **Milestone 2** of the
project brief. Below is exactly what was broken, what was missing, and what
was added — plus how to run it.

## What was broken

- **The app couldn't start.** `database.py` pointed at `database/examguard.db`
  while the uploaded `database.db` sat unused at the project root, and
  `init_db()` had every `CREATE TABLE` statement commented out while still
  running `SELECT * FROM browser_events` — a table that never existed. First
  run would crash with `no such table: browser_events`.
- **Registration would fail.** The `candidates` table had no `photo` column
  (the `ALTER TABLE` for it was commented out), but the insert statement
  wrote to it anyway.
- **`app.py` imported a package that didn't exist.** `monitoring.face_monitor`
  and `monitoring.face_logger` were referenced but never uploaded.
- **`exam.html` was wrapped in Markdown code fences** (` ```html ... ``` `),
  which would have rendered as literal text in the browser.
- **`requirements.txt` was empty.**

## What was missing (Milestone 2 gaps)

- **`monitoring/face_monitor.py`** — OpenCV Haar Cascade face-presence
  detection (`detect_face`), using the pre-trained classifier that ships with
  OpenCV, per the brief (no model training required).
- **`monitoring/face_logger.py`** — tracks face-absent *intervals*, not just
  point-in-time states: opens a row when a face first goes missing, and closes
  it with `ended_at` / `duration_seconds` once the face reappears.
- **`monitoring/event_detector.py`** — the rule-based suspicious event
  detection engine called for in the brief, with configurable thresholds:
  - more than 3 tab switches → flagged
  - face absent for more than 2 minutes (continuous) → flagged
  - more than 5 focus-loss events within a 5-minute window → flagged

  Flags are written to a new `suspicious_events` table with a plain-language
  `reason` an invigilator can read directly.
- **Exam session lifecycle** (start / pause / resume / submit) — Milestone 1
  calls for this explicitly. Added an `exam_sessions` table and
  `/pause-exam`, `/resume-exam`, `/submit-exam` routes, plus buttons on the
  exam page.
- **`synthetic_data_generator.py`** — the Faker-based synthetic session data
  generator described as the "Week 1 warm-up task." `partice.py` was Faker
  practice code, not this deliverable, so it's left alone and this new script
  writes realistic candidates + `exam_sessions` + `browser_events` +
  `face_events` rows using the *actual* production schema — useful once you
  reach the Milestone 3 scoring/analytics work.
- **`requirements.txt`** filled in.

## UI

All pages now share `static/css/style.css` and a common navbar
(`templates/base.html`). Login, register and the dashboard use a plain,
paper-toned card layout; the exam page keeps a live "console" style event
log so invigilator-relevant activity (tab switches, focus loss, copy/paste,
right-click) is visually distinct from routine activity.

## Project structure

```
app.py                      Flask routes
database.py                 SQLite connection + schema (all tables)
camera.py                   Saves webcam-captured registration photos
synthetic_data_generator.py Faker-based fake session data (Milestone 1)
requirements.txt

monitoring/
  face_monitor.py           Haar Cascade face presence detection
  face_logger.py            Face-absent interval tracking
  event_detector.py         Rule-based suspicious event engine

templates/
  base.html, login.html, register.html, dashboard.html, exam.html

static/
  css/style.css
  uploads/                  Registration photos land here
```

## Running it

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

The database file is created automatically at `database/examguard.db` on
first run — the old `database.db` in your original upload is no longer used
and can be deleted.

To generate test data for later milestones without running real exams:

```bash
python synthetic_data_generator.py 20   # 20 fake candidates + sessions
```

## Verified

I ran this end-to-end (register → login → dashboard → start exam → face
monitoring → browser event logging → rule engine firing a flag → pause →
resume → submit) with Flask's test client before handing it back, so the
whole Milestone 1–2 flow is confirmed working, not just written.

## Left as-is

- `partice.py` — your personal Python/Faker practice file, unrelated to the
  ExamGuard schema. Not touched.
- Everything from Milestone 3 onward (integrity scoring, the LangChain
  report agent, Data Science analytics, the Streamlit dashboard, JSON/CSV
  export) is intentionally out of scope here, since you asked for Milestone
  1–2 completion only.
