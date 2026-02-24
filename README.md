[5/50]

```markdown
# People API – FastAPI + SQLAlchemy + Alembic

A production-structured REST API built with **FastAPI**, **SQLAlchemy**, **SQLite**, and **Alembic**.

This project demonstrates clean backend architecture, service-layer orchestration, transaction management, database migrations, validation discipline, and production-ready development patterns.

The project is actively evolving.

---

# 🚀 Overview

This API manages a `Person` resource while demonstrating:

- Layered architecture (API → Service → CRUD → ORM)
- Pydantic v2 validation with strict PATCH handling
- Transaction-safe service orchestration
- Custom exception handling
- Audit logging
- Email outbox pattern
- Alembic migrations (schema versioning)
- SQLite-safe schema evolution

---

# 🧱 Tech Stack

- Python
- FastAPI
- SQLAlchemy ORM
- Pydantic v2
- SQLite
- Alembic (database migrations)
- Uvicorn (ASGI server)

---

# 📂 Project Structure

```

.
├── main.py                # FastAPI app and routes
├── database.py            # Engine, SessionLocal, Base
├── models.py              # SQLAlchemy ORM models
├── schemas.py             # Pydantic schemas (validation layer)
├── crud.py                # Pure DB operations
├── services.py            # Business logic + transactions
├── exceptions.py          # Custom domain exceptions
├── alembic.ini            # Alembic configuration
├── alembic/               # Migration environment
│   └── versions/          # Versioned migration scripts
├── people.db              # SQLite database
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

SQLite is configured with:

```

check_same_thread=False

```

to allow usage within FastAPI’s async environment.

---

## 2️⃣ ORM Models

**models.py**

### PersonDB
- id (PK)
- name (unique, indexed)
- age
- email

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

## 3️⃣ Alembic Migrations (Active)

This project now uses **Alembic for schema versioning**.

### Example Migration Implemented

`add_email_to_person`

- Adds `email` column to `people`
- Backfills existing rows
- Safely alters column nullability (SQLite batch mode)
- Enforces NOT NULL constraint

This demonstrates:

- Forward-compatible schema evolution
- Safe SQLite alteration strategy
- Controlled database upgrades and downgrades

---

## 4️⃣ Pydantic Schemas

**schemas.py**

### PersonBase
- name (2–50 characters)
- age (0–120)

### PersonCreate
Used for POST

### PersonUpdate
Used for PUT (full replacement)

### PersonPatch
Used for PATCH (partial update)

PATCH Safety Rules:

- Rejects explicit null values
- Requires at least one field
- Validates provided fields strictly

### Response Schemas

- PersonResponse
- AuditLogResponse
- EmailOutboxResponse

Configured with:

```

from_attributes = True

```

---

## 5️⃣ CRUD Layer

**crud.py**

Responsible for pure database operations only:

- create_person
- get_people (with filtering + pagination)
- get_person
- update_person
- patch_person
- delete_person
- create_audit_log
- create_email_outbox

No transaction control logic exists here.

---

## 6️⃣ Service Layer

**services.py**

Handles:

- Transaction control
- Orchestration of:
  - Person creation
  - Audit log creation
  - Email outbox creation
- Rollbacks on failure
- IntegrityError handling
- Raising domain-level exceptions

Example flow:

```

Create Person
→ Flush (assign ID)
→ Create Audit Log
→ Create Email Outbox record
→ Commit

```

This demonstrates real-world service orchestration patterns.

---

## 7️⃣ FastAPI Application

**main.py**

Includes:

- Dependency-injected DB session
- RESTful endpoints
- Centralized exception handler
- Health check endpoint
- Integration with service layer

---

# 🔌 API Endpoints

## Health
```

GET /health

```

---

## Create Person
```

POST /people

```

---

## Get All People
Supports:
- skip
- limit
- min_age
- name_contains

```

GET /people

```

---

## Get Person By ID
```

GET /people/{person_id}

```

---

## Update Person (Full Replace)
```

PUT /people/{person_id}

```

---

## Patch Person (Partial Update)
```

PATCH /people/{person_id}

```

---

## Delete Person
```

DELETE /people/{person_id}

```

---

# ⚙️ Running the Project

## 1️⃣ Create Virtual Environment

```

python -m venv venv

```

Activate:

Windows:
```

venv\Scripts\activate

```

Mac/Linux:
```

source venv/bin/activate

```

---

## 2️⃣ Install Dependencies

```

pip install fastapi uvicorn sqlalchemy alembic

```

---

## 3️⃣ Run Database Migrations

Initialize database to latest schema:

```

alembic upgrade head

```

Check migration history:

```

alembic history

```

Generate new migration:

```

alembic revision --autogenerate -m "your message"

```

Apply migration:

```

alembic upgrade head

```

---

## 4️⃣ Start the Server

```

uvicorn main:app --reload

```

Access:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

---

# 🧠 Backend Engineering Concepts Demonstrated

- Layered architecture
- Transaction boundaries
- Database migrations
- Service orchestration
- Domain exception handling
- Validation beyond type checking
- Email outbox pattern
- Audit trail pattern
- SQLite-safe schema evolution
- Clean separation of concerns

---

# 🛠 Roadmap

Planned improvements:

- Unit tests (pytest)
- Integration tests
- Background email processor
- Structured logging
- Dockerization
- Environment configuration separation
- Authentication (JWT)
- CI/CD pipeline
- Production database support (PostgreSQL)

---

# 🎯 Role Alignment

This project demonstrates patterns expected in:

- Backend Developer roles
- API Engineer roles
- Python Developer roles
- Junior → Mid-level Backend Engineering positions

Key competencies showcased:

- API design
- Schema evolution
- Transaction handling
- Data modeling
- Validation strategy
- Service abstraction
- Migration management

---

# 📌 Status

Active development.

Schema migrations are now version-controlled via Alembic.

Architecture is intentionally structured for production scalability.
```
