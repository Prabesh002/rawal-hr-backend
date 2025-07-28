from sqlalchemy import Column, Date, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.Entities.BaseEntity import BaseEntity
from sqlalchemy.dialects.postgresql import UUID

class PayrollEntity(BaseEntity):
    __tablename__ = "payrolls"
    __table_args__ = {"schema": "hr"}

    employee_id = Column(UUID(as_uuid=True), ForeignKey("hr.employees.id"), nullable=False, index=True)
    
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    payment_date = Column(Date, nullable=True)

    total_hours = Column(Numeric(10, 2), nullable=False)
    gross_pay = Column(Numeric(12, 2), nullable=False)
    deductions = Column(Numeric(12, 2), default=0.00)
    net_pay = Column(Numeric(12, 2), nullable=False)
    
    status = Column(String(50), nullable=False, default="Pending") 

    employee = relationship("EmployeeEntity", back_populates="payrolls")