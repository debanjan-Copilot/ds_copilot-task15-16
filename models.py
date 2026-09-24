from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Department(Base):
    __tablename__ = "department_DS"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    faculties = relationship("Faculty", back_populates="department")


class Faculty(Base):
    __tablename__ = "faculty_DS"

    faculty_id = Column(String(50), primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    department_id = Column(Integer, ForeignKey("department_DS.department_id"), nullable=False, index=True)
    designation = Column(String(255), nullable=False)
    joining_date = Column(Date, nullable=True)
    courses_taught = Column(Text, nullable=True)
    experience_history = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    department = relationship("Department", back_populates="faculties")
