from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import crud
import schemas
from exceptions import NameAlreadyExistsException

def create_person_service(db: Session, person: schemas.PersonCreate):
    try:
        db_person = crud.create_person(db, person)

        db.flush()
        # flush sends staged INSERTs so db_person.id is assigned before commit

        crud.create_audit_log(db, action="person_created", person_id=db_person.id)
        crud.create_email_outbox(db, person_id=db_person.id, email_type="welcome")

        db.commit()
        db.refresh(db_person)
        return db_person

    except IntegrityError:
        db.rollback()
        raise NameAlreadyExistsException()

    except:
        db.rollback()
        raise