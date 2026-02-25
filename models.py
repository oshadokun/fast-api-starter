from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class PersonDB(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    
class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)

class EmailOutboxDB(Base):
    __tablename__ = "email_outbox"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    email_type = Column(String, nullable=False)          # example: "welcome"
    status = Column(String, nullable=False, default="pending")  # pending, sent, failed
    retry_count = Column(Integer, nullable=False, default=0)