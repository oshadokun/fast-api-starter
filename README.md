
# People API – FastAPI + SQLAlchemy Backend

A production-style REST API built with **FastAPI**, **SQLAlchemy**, and **SQLite**, designed to demonstrate clean backend architecture, validation, transaction handling, and service-layer orchestration.

This project is ongoing and will evolve with additional features, refactoring, and test coverage.

---

## 🚀 Overview

This API manages a simple **Person** resource while demonstrating:

- Layered architecture (API → Service → CRUD → DB)
- Pydantic validation (including PATCH safety rules)
- Transaction-safe service logic
- Exception handling
- Audit logging
- Email outbox pattern (async-ready design)
- SQLite integration with SQLAlchemy ORM

---

## 🧱 Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy ORM**
- **Pydantic v2**
- **SQLite**
- Uvicorn (ASGI server)

---

## 📂 Project Structure

```

.
├── main.py          # FastAPI app + route definitions
├── database.py      # Engine + SessionLocal + Base
├── models.py        # SQLAlchemy ORM models
├── schemas.py       # Pydantic request/response schemas
├── crud.py          # Database access layer
├── services.py      # Business logic layer
├── exceptions.py    # Custom exceptions
├── people.db        # SQLite database file

```

---

## 🏗 Architecture

### 1️⃣ Database Configuration

SQLite database configured in:

`database.py` :contentReference[oaicite:0]{index=0}

- Uses `SessionLocal`
- Declarative `Base`
- Thread-safe SQLite configuration

---

### 2️⃣ ORM Models

Defined in:

`models.py` :contentReference[oaicite:1]{index=1}

Tables:

- `people`
- `audit_logs`
- `email_outbox`

This supports:
- Unique person names
- Audit trail tracking
- Email outbox pattern for async processing

---

### 3️⃣ Pydantic Schemas

Defined in:

`schemas.py` :contentReference[oaicite:2]{index=2}

Includes:

- `PersonCreate`
- `PersonUpdate` (PUT)
- `PersonPatch` (PATCH with strict validation)
- `PersonResponse`

PATCH safety features:
- Rejects explicit `null`
- Requires at least one field
- Field-level validation enforced

---

### 4️⃣ CRUD Layer

Defined in:

`crud.py` :contentReference[oaicite:3]{index=3}

Handles:

- Create person
- Query with filtering and pagination
- Update (PUT)
- Patch (partial update)
- Delete
- Audit log creation
- Email outbox entry creation

This layer performs **pure DB operations only**.

---

### 5️⃣ Service Layer

Defined in:

`services.py` :contentReference[oaicite:4]{index=4}

Responsibilities:

- Transaction control
- Orchestrating:
  - Person creation
  - Audit log entry
  - Email outbox record
- Proper rollback handling
- Raising domain-level exceptions

Example flow:
```

Create Person
→ Flush to assign ID
→ Create Audit Log
→ Create Email Outbox entry
→ Commit

```

---

### 6️⃣ FastAPI Application

Defined in:

`main.py` :contentReference[oaicite:5]{index=5}

Features:

- Dependency injection for DB session
- RESTful endpoints
- Centralized exception handling
- Health check endpoint

---

## 🔌 API Endpoints

### Health
```

GET /health

```

---

### Create Person
```

POST /people

```

---

### Get All People
Supports:
- Pagination (`skip`, `limit`)
- Filtering (`min_age`, `name_contains`)

```

GET /people

```

---

### Get Person By ID
```

GET /people/{person_id}

```

---

### Update Person (Full Replace)
```

PUT /people/{person_id}

```

---

### Patch Person (Partial Update)
```

PATCH /people/{person_id}

```

---

### Delete Person
```

DELETE /people/{person_id}

````

---

## ⚙️ Running the Project

### 1️⃣ Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy
````

If using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

---

### 2️⃣ Run the Server

```bash
uvicorn main:app --reload
```

Access:

* API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧠 Backend Concepts Demonstrated

* Clean separation of concerns
* Service-layer transaction orchestration
* Domain exception handling
* Validation beyond basic type checking
* Email outbox pattern
* Audit logging
* Safe PATCH implementation
* Unique constraint enforcement

---

## 🛠 Future Improvements (Planned)

* Unit tests (pytest)
* Integration tests
* Async email processor worker
* JWT authentication
* Dockerization
* Migration tool (Alembic)
* Logging strategy
* Structured error responses
* CI/CD pipeline
* Production-ready config management

---

## 🎯 Why This Project Matters

This project demonstrates:

* Real backend engineering patterns
* API design fundamentals
* Database integrity handling
* Clean architecture principles
* Readiness for production evolution

It is structured intentionally to align with **backend engineering / API development roles**, showcasing:

* Transaction handling
* Data modeling
* Validation discipline
* Exception control
* Layered architecture

---

## 📌 Status

Active development.
Design decisions may evolve as features expand.

---

```
```
