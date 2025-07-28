from sqlalchemy import Column, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from app.Entities.BaseEntity import BaseEntity
from sqlalchemy.dialects.postgresql import UUID

class AttendanceEntity(BaseEntity):
    __tablename__ = "attendances"
    __table_args__ = {"schema": "hr"}

    employee_id = Column(UUID(as_uuid=True), ForeignKey("hr.employees.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)

    employee = relationship("EmployeeEntity", back_populates="attendances")