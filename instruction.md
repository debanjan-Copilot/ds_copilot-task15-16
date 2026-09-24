# Faculty Information System

## 1. Project Purpose
This project is a FastAPI-based faculty information management system. It stores faculty records and departmental metadata for academic institutions.

## 2. Architecture Guidelines
- Controller layer handles HTTP requests, validation, and response formatting.
- Service layer contains business logic.
- Repository layer encapsulates SQLAlchemy data access.
- Services depend on repository contracts rather than database implementations.
- Services raise application-level errors; the API layer translates them into HTTP responses.
- Models define Department and Faculty entities.
- Database configuration manages engine and sessions.

## 3. Coding Standards
- Use meaningful names and focused functions.
- Prefer small, readable functions.
- Use type hints.
- Prefer constructor dependency injection over hidden global state.
- Keep imports organized and remove unused imports.
- Handle errors explicitly.
- Keep code easy to test and maintain.

## 4. Database Integration Rules
- Use SQLAlchemy ORM with PostgreSQL.
- Allow `DATABASE_URL`, `DB_CONNECT_TIMEOUT`, and `DB_SSLMODE` environment overrides.
- Use the `faculty_db` database by default.
- Use explicit model definitions and `_DS` table names.
- Maintain the one-to-many Department-Faculty relationship.
- Close sessions correctly and roll back failed writes.

## 5. Model Requirements
Department fields include `department_id`, `department_name`, `description`, `created_at`, and `updated_at`.

Faculty fields include `faculty_id`, `full_name`, `email`, `phone`, `date_of_birth`, `department_id`, `designation`, `joining_date`, `courses_taught`, `experience_history`, `status`, `created_at`, and `updated_at`.

## 6. Testing Guidelines
- Test service logic and repository behavior.
- Test API endpoints where feasible.
- Cover success, validation, not-found, conflict, and database error scenarios.
- Keep tests isolated and deterministic.
- Use pytest.
