from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DepartmentCreate(BaseModel):
    department_id: Optional[int] = Field(default=None, gt=0)
    department_name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None


class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = Field(default=None, min_length=2, max_length=255)
    description: Optional[str] = None


class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class FacultyCreate(BaseModel):
    faculty_id: str = Field(..., min_length=1, max_length=50, pattern=r"^[A-Za-z0-9_-]+$")
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=20)
    date_of_birth: Optional[date] = None
    department_id: int = Field(..., gt=0)
    designation: str = Field(..., min_length=2, max_length=255)
    joining_date: Optional[date] = None
    courses_taught: Optional[str] = None
    experience_history: Optional[str] = None
    status: str = Field(default="Active", max_length=50)


class FacultyUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)
    date_of_birth: Optional[date] = None
    department_id: Optional[int] = Field(default=None, gt=0)
    designation: Optional[str] = Field(default=None, min_length=2, max_length=255)
    joining_date: Optional[date] = None
    courses_taught: Optional[str] = None
    experience_history: Optional[str] = None
    status: Optional[str] = Field(default=None, max_length=50)


class FacultyResponse(BaseModel):
    faculty_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    department_id: int
    designation: str
    joining_date: Optional[date] = None
    courses_taught: Optional[str] = None
    experience_history: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
