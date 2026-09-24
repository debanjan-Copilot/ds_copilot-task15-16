from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from repositories.department_repository import DepartmentRepository
from schemas import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from services.department_service import DepartmentService

router = APIRouter(prefix="/api/departments", tags=["departments"])


def get_department_service(db: Session = Depends(get_db)) -> DepartmentService:
    return DepartmentService(DepartmentRepository(db))


@router.get("", response_model=list[DepartmentResponse])
def get_departments(service: DepartmentService = Depends(get_department_service)):
    return service.get_all_departments()


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: int, service: DepartmentService = Depends(get_department_service)):
    return service.get_department_by_id(department_id)


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(department: DepartmentCreate, service: DepartmentService = Depends(get_department_service)):
    return service.create_department(department)


@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(department_id: int, department: DepartmentUpdate, service: DepartmentService = Depends(get_department_service)):
    return service.update_department(department_id, department)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, service: DepartmentService = Depends(get_department_service)):
    service.delete_department(department_id)
