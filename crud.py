
import models
import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from exceptions import NameAlreadyExistsException


from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas
from exceptions import NameAlreadyExistsException

def create_person(db: Session, person: schemas.PersonCreate) -> models.PersonDB:
    existing = db.query(models.PersonDB).filter(models.PersonDB.name == person.name).first()
    if existing:
        raise NameAlreadyExistsException()

    db_person = models.PersonDB(name=person.name, age=person.age)
    db.add(db_person)
    return db_person

def create_audit_log(db: Session, action: str, person_id: int) -> models.AuditLogDB:
    log = models.AuditLogDB(action=action, person_id=person_id)
    db.add(log)
    return log

def create_email_outbox(db: Session, person_id: int, email_type: str = "welcome") -> models.EmailOutboxDB:
    outbox = models.EmailOutboxDB(person_id=person_id, email_type=email_type, status="pending", retry_count=0)
    db.add(outbox)
    return outbox

def get_people(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_age: int | None = None,
    name_contains: str | None = None,
) -> list[models.PersonDB]:
    query = db.query(models.PersonDB)

    if min_age is not None:
        query = query.filter(models.PersonDB.age >= min_age)

    if name_contains:
        query = query.filter(models.PersonDB.name.ilike(f"%{name_contains}%"))

    return query.offset(skip).limit(limit).all()

def get_person(db: Session, person_id: int):
    return db.query(models.PersonDB).filter(models.PersonDB.id == person_id).first()
def update_person(
    db: Session,
    person_id: int,
    updated: schemas.PersonUpdate,
) -> models.PersonDB | None:
    person = get_person(db, person_id)
    if person is None:
        return None

    person.name = updated.name
    person.age = updated.age

    db.commit()
    db.refresh(person)
    return person


def delete_person(db: Session, person_id: int) -> bool:
    person = get_person(db, person_id)
    if person is None:
        return False

    db.delete(person)
    db.commit()
    return True

def patch_person(
    db: Session,
    person_id: int,
    patch: schemas.PersonPatch,
) -> models.PersonDB | None:
    person = get_person(db, person_id)
    if person is None:
        return None

    patch_data = patch.model_dump(exclude_unset=True)

    # Safety: reject explicit null attempts like {"name": null}
   
    for field, value in patch_data.items():
        setattr(person, field, value)

    db.commit()
    db.refresh(person)
    return person
