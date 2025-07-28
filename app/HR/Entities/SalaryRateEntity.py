from sqlalchemy import Column, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.Entities.BaseEntity import BaseEntity
from sqlalchemy.dialects.postgresql import UUID

class SalaryRateEntity(BaseEntity):
    __tablename__ = "salary_rates"
    __table_args__ = {"schema": "hr"}

    employee_id = Column(UUID(as_uuid=True), ForeignKey("hr.employees.id"), nullable=False, index=True)
    hourly_rate = Column(Numeric(10, 2), nullable=False)
    effective_date = Column(Date, nullable=False)

    employee = relationship("EmployeeEntity", back_populates="salary_rates")