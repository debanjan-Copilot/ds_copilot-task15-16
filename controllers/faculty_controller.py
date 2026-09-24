from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from repositories.department_repository import DepartmentRepository
from repositories.faculty_repository import FacultyRepository
from schemas import FacultyCreate, FacultyResponse, FacultyUpdate
from services.faculty_service import FacultyService

router = APIRouter(prefix="/api", tags=["faculties"])


def get_faculty_service(db: Session = Depends(get_db)) -> FacultyService:
    return FacultyService(FacultyRepository(db), DepartmentRepository(db))


@router.get("/faculties", response_model=list[FacultyResponse])
def get_faculties(service: FacultyService = Depends(get_faculty_service)):
    return service.get_all_faculties()


@router.get("/faculties/{faculty_id}", response_model=FacultyResponse)
def get_faculty(faculty_id: str, service: FacultyService = Depends(get_faculty_service)):
    return service.get_faculty_by_id(faculty_id)


@router.post("/faculties", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
def create_faculty(faculty: FacultyCreate, service: FacultyService = Depends(get_faculty_service)):
    return service.create_faculty(faculty)


@router.put("/faculties/{faculty_id}", response_model=FacultyResponse)
def update_faculty(faculty_id: str, faculty: FacultyUpdate, service: FacultyService = Depends(get_faculty_service)):
    return service.update_faculty(faculty_id, faculty)


@router.delete("/faculties/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty(faculty_id: str, service: FacultyService = Depends(get_faculty_service)):
    service.delete_faculty(faculty_id)
