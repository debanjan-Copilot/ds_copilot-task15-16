# Faculty Information System

A FastAPI and PostgreSQL application for managing departments and faculty records.

## Features

- Layered Controller, Service, and Repository architecture.
- PostgreSQL integration through SQLAlchemy.
- CRUD REST APIs for departments and faculty.
- Validation with Pydantic.
- Application-level error handling.
- Jinja2 web frontend.
- Responsive HTML/CSS/JavaScript frontend for managing faculty and departments.
- Unit tests for service and controller layers.
- SQL schema included in [`schema.sql`](./schema.sql).
- Configurable AI pull-request review agent through GitHub Actions.
- Local `Bug Investigator` custom agent for reproducible bug fixes.

## Project Structure

```text
faculty_info_system/
├── controllers/       # HTTP route handlers
├── repositories/      # Data access implementations and contracts
├── services/          # Business logic
├── templates/          # Jinja2 frontend
├── static/             # Frontend CSS and JavaScript
├── tests/             # Unit tests
├── database.py        # SQLAlchemy engine and sessions
├── models.py          # Department and Faculty ORM models
├── schemas.py         # Request and response validation schemas
├── schema.sql         # PostgreSQL DDL
├── seed_data.py       # Optional sample data loader
├── instruction.md     # Architecture and coding guidelines
└── main.py            # FastAPI application entry point
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database connection. The default target is:

   ```text
   postgresql+psycopg2://postgres@172.16.51.63:5432/faculty_db
   ```

   Prefer setting `DATABASE_URL` rather than hardcoding credentials. Optional settings:

   - `DB_CONNECT_TIMEOUT`
   - `DB_SSLMODE`

4. Apply [`schema.sql`](./schema.sql) if tables are not already created.

For local frontend development without access to the remote PostgreSQL server, you can use SQLite:

```powershell
$env:DATABASE_URL = "sqlite:///./faculty_info_system_local.db"
python seed_data.py
python -m uvicorn main:app --reload
```

This local mode is for development only. PostgreSQL remains the default production database.

## Run

```bash
uvicorn main:app --reload
```

Open the frontend at `http://localhost:8000` and API documentation at `http://localhost:8000/docs`.

## API Endpoints

### Departments

- `GET /api/departments`
- `GET /api/departments/{department_id}`
- `POST /api/departments`
- `PUT /api/departments/{department_id}`
- `DELETE /api/departments/{department_id}`

### Faculty

- `GET /api/faculties`
- `GET /api/faculties/{faculty_id}`
- `POST /api/faculties`
- `PUT /api/faculties/{faculty_id}`
- `DELETE /api/faculties/{faculty_id}`

## Tests

Run the unit tests without requiring a live database:

```bash
python -m pytest -q tests
```

## AI PR Agent

The `AI PR Agent` workflow reviews pull requests, includes the test outcome, and posts findings as a pull-request comment. Configure repository secret `AI_API_URL`, repository secret `AI_API_KEY`, and repository variable `AI_MODEL` before enabling it. The workflow uses the GitHub token only to read the pull-request diff and post the generated review comment. It does not send database credentials or source secrets to the model endpoint.

## Bug Investigator Agent

The local custom agent definition is available at `.github/agents/bug-investigator.agent.md`. Use it when a bug report needs root-cause analysis and a code fix. The agent is instructed to reproduce the issue, trace the layered architecture, add a regression test, implement a minimal fix, run tests, and report unresolved limitations.

## Documentation

See [`instruction.md`](./instruction.md) for project purpose, architecture, coding standards, database rules, and testing guidance.
