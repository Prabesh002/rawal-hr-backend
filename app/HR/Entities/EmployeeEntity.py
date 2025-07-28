from sqlalchemy import Column, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.Entities.BaseEntity import BaseEntity

class EmployeeEntity(BaseEntity):
    __tablename__ = "employees"
    __table_args__ = {"schema": "hr"}

    user_id = Column(ForeignKey("users.users.id"), nullable=True, unique=True)
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    position = Column(String(100), nullable=False)
    hire_date = Column(Date, nullable=False)
    termination_date = Column(Date, nullable=True)

    user = relationship("User")
    attendances = relationship("AttendanceEntity", back_populates="employee", cascade="all, delete-orphan")
    time_logs = relationship("TimeLogEntity", back_populates="employee", cascade="all, delete-orphan")
    salary_rates = relationship("SalaryRateEntity", back_populates="employee", cascade="all, delete-orphan")
    payrolls = relationship("PayrollEntity", back_populates="employee", cascade="all, delete-orphan")