
# People API – FastAPI + SQLAlchemy + Alembic + Pytest
---

# 🏛 Clean Architecture Overview

```

```
            ┌────────────────────────────┐
            │        Client (HTTP)       │
            │  Swagger / Browser / Test  │
            └──────────────┬─────────────┘
                           │
                           ▼
            ┌────────────────────────────┐
            │        main.py             │
            │  Route Layer (FastAPI)     │
            │  - Request validation      │
            │  - Dependency injection    │
            │  - Exception translation   │
            └──────────────┬─────────────┘
                           │
                           ▼
            ┌────────────────────────────┐
            │       services.py          │
            │  Service Layer             │
            │  - Transaction boundary    │
            │  - Orchestration           │
            │  - IntegrityError mapping  │
            │  - Commit / Rollback       │
            └──────────────┬─────────────┘
                           │
                           ▼
            ┌────────────────────────────┐
            │        crud.py             │
            │  Data Access Layer         │
            │  - Pure DB operations      │
            │  - No commits              │
            │  - No HTTP logic           │
            └──────────────┬─────────────┘
                           │
                           ▼
            ┌────────────────────────────┐
            │        models.py           │
            │  SQLAlchemy ORM            │
            │  - Tables                  │
            │  - Constraints             │
            │  - Relationships           │
            └──────────────┬─────────────┘
                           │
                           ▼
            ┌────────────────────────────┐
            │         SQLite DB          │
            │  - PRIMARY KEY             │
            │  - UNIQUE constraints      │
            │  - Foreign Keys            │
            └────────────────────────────┘
```

```

### Design Principles Enforced

- Clear separation of concerns
- Database constraints as source of truth
- Service layer owns transactions
- CRUD layer never commits
- Routes never contain business logic
- Errors translated at the correct abstraction level
- Tests validate behavior at HTTP boundary

---

A production-structured REST API built with **FastAPI**, **SQLAlchemy**, **SQLite**, **Alembic**, and **Pytest**.

This project demonstrates clean backend architecture, service-layer orchestration, transaction management, database migrations, validation discipline, automated testing, and production-ready development patterns.

The project is actively evolving.

---

# 🚀 Overview

This API manages a `Person` resource while demonstrating:

- Layered architecture (API → Service → CRUD → ORM)
- Pydantic v2 validation with strict PATCH handling
- Email validation using `EmailStr`
- Database-level uniqueness enforcement
- Transaction-safe service orchestration
- Custom domain exception handling
- Audit logging pattern
- Email outbox pattern
- Alembic migrations (schema versioning)
- SQLite-safe schema evolution
- Automated API testing with pytest

---

# 🧱 Tech Stack

- Python
- FastAPI
- SQLAlchemy ORM
- Pydantic v2
- SQLite
- Alembic (database migrations)
- Pytest (automated testing)
- HTTPX (test client)
- Uvicorn (ASGI server)

---

# 📂 Project Structure

```

.
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── services.py
├── exceptions.py
├── alembic.ini
├── alembic/
│   └── versions/
├── tests/
│   ├── conftest.py
│   └── test_people_api.py
├── people.db
├── .gitignore
└── README.md

```

---

# 🏗 Architecture

## 1️⃣ Database Layer

**database.py**

- SQLite database
- SQLAlchemy engine
- SessionLocal factory
- Declarative Base

SQLite configured with:

```

check_same_thread=False

```

---

## 2️⃣ ORM Models

**models.py**

### PersonDB
- id (PK)
- name (unique, indexed, NOT NULL)
- age (NOT NULL)
- email (unique, indexed, NOT NULL)

Email uniqueness enforced at the database level.

### AuditLogDB
- id
- action
- person_id (FK → people.id)

### EmailOutboxDB
- id
- person_id (FK)
- email_type
- status
- retry_count

---

## 3️⃣ Alembic Migrations

This project uses Alembic for schema versioning.

Email column migration demonstrates:

- Backfill strategy
- SQLite batch mode
- Constraint enforcement
- Safe NOT NULL transition
- UNIQUE constraint addition

---

## 4️⃣ Pydantic Schemas

**schemas.py**

- Email validation via `EmailStr`
- Strict PATCH validation rules
- PUT vs PATCH separation
- Response serialization via `from_attributes = True`

---

## 5️⃣ CRUD Layer

- Pure DB access
- No transaction logic
- No HTTP knowledge

---

## 6️⃣ Service Layer

- Controls transaction boundaries
- Handles IntegrityError
- Converts DB errors → domain exceptions
- Orchestrates multi-step writes
- Commits only after successful orchestration

---

## 7️⃣ FastAPI Application

- Dependency-injected sessions
- Centralized exception handlers
- RESTful endpoints
- Clean HTTP error responses

---

# 🧪 Automated Testing

- Separate test database
- Dependency override for `get_db`
- Nested transaction rollback per test
- API-level behavior validation

Run:

```

pytest -v

```

---

# ⚙️ Running the Project

Create environment:

```

python -m venv .venv

```

Install:

```

pip install fastapi uvicorn sqlalchemy alembic pytest httpx "pydantic[email]"

```

Migrate:

```

alembic upgrade head

```

Run:

```

uvicorn main:app --reload

```

---

# 🧠 Engineering Concepts Demonstrated

- Transaction boundaries
- IntegrityError mapping
- Database-first validation
- Service-layer orchestration
- Migration discipline
- Automated API testing
- Layered backend architecture

---

# 📌 Status

Active development.
Production-structured architecture.
Database constraints enforced.
Service-layer transaction control implemented.
Automated test coverage active.
```

---

If you want, I can next:

* Convert that diagram into a visual PNG/SVG diagram
* Or add a test-flow diagram section
* Or add a transaction lifecycle diagram

You're now writing README like a mid-level backend engineer.
