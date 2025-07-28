from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.Entities.BaseEntity import BaseEntity
from sqlalchemy.dialects.postgresql import UUID

class TimeLogEntity(BaseEntity):
    __tablename__ = "time_logs"
    __table_args__ = {"schema": "hr"}

    employee_id = Column(UUID(as_uuid=True), ForeignKey("hr.employees.id"), nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)

    employee = relationship("EmployeeEntity", back_populates="time_logs")