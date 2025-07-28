import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.Core.Database.ApplicationDatabaseContext import Base
from sqlalchemy.orm import declarative_base, declared_attr
class Base:
    @declared_attr
    def __tablename__(cls):
        import re
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower() + "s" #lowercase ma convert garne every table so used regex [Copilot suggested]


Base = declarative_base(cls=Base)

class BaseEntity(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())