import crud
from sqlalchemy.exc import IntegrityError
from exceptions import NameAlreadyExistsException, EmailAlreadyExistsException


def create_person_service(db, person_in):
    try:
        # create person
        db_person = crud.create_person(db, person_in)

        # create related records if any
        # ...

        db.commit()
        db.refresh(db_person)
        return db_person

    except IntegrityError as e:
        db.rollback()

        msg = str(getattr(e, "orig", e))

        if "UNIQUE constraint failed: people.name" in msg:
            raise NameAlreadyExistsException()

        if "UNIQUE constraint failed: people.email" in msg:
            raise EmailAlreadyExistsException()

        raise

    except Exception:
        db.rollback()
        raise