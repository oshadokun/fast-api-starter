from pydantic import BaseModel, Field, field_validator,  model_validator
from typing import Optional


class PersonBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=0, le=120)


class PersonCreate(PersonBase):
    pass

# PUT: full update, all required
class PersonUpdate(PersonBase):
    pass

# PATCH: partial update, all optional, but still validated if provided
class PersonPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=120)


    @field_validator("name",mode="before")
    @classmethod
    def name_cannot_be_null(cls, v):
        if v is None:
            raise ValueError("name cannot be null")
        return v

    @field_validator("age",mode="before")
    @classmethod
    def age_cannot_be_null(cls, v):
        if v is None:
            raise ValueError("age cannot be null")
        return v
    
    @model_validator(mode="after")
    def at_least_one_field(self):
        if not self.model_dump(exclude_unset=True):
            raise ValueError("At least one field must be provided for PATCH")
        return self

class PersonResponse(PersonBase):
    id: int

    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: int
    action: str
    person_id: int

    class Config:
        from_attributes = True

class EmailOutboxResponse(BaseModel):
    id: int
    person_id: int
    email_type: str
    status: str
    retry_count: int

    class Config:
        from_attributes = True
