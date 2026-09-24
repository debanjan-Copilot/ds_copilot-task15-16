# Faculty Information System

A FastAPI and PostgreSQL application for managing departments and faculty records.

## Features

- Layered Controller, Service, and Repository architecture.
- PostgreSQL integration through SQLAlchemy.
- CRUD REST APIs for departments and faculty.
- Validation with Pydantic.
- Application-level error handling.
- Jinja2 web frontend.
- Unit tests for service and controller layers.
- SQL schema included in `schema.sql`.

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Configure `DATABASE_URL`, `DB_CONNECT_TIMEOUT`, and `DB_SSLMODE` as needed. The default database is `faculty_db`.

API documentation is available at `/docs`.

## Tests

```bash
python -m pytest -q tests
```

See `instruction.md` for architecture, coding, database, and testing guidelines.