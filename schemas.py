# schemas.py (Day 11: keep validation, add email, keep PATCH rules)

from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict
from typing import Optional


class PersonBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=0, le=120)
    email: EmailStr


class PersonCreate(PersonBase):
    pass


# PUT: full update, all required
class PersonUpdate(PersonBase):
    pass


# PATCH: partial update, all optional, but validated if provided
class PersonPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=120)
    email: Optional[EmailStr] = None

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        # values is the model instance in Pydantic v2 "after" mode
        if values.name is None and values.age is None and values.email is None:
            raise ValueError("PATCH payload must include at least one field")
        return values


class PersonResponse(PersonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Optional: if you already have these in your project, keep them here too.
class AuditLogResponse(BaseModel):
    id: int
    action: str
    person_id: int
    model_config = ConfigDict(from_attributes=True)


class EmailOutboxResponse(BaseModel):
    id: int
    to_email: str
    subject: str
    body: str
    status: str
    model_config = ConfigDict(from_attributes=True)