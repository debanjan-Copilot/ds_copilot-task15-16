from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from errors import ConflictError, DatabaseUnavailableError, ResourceNotFoundError, ValidationError
from models import Department
from repositories.contracts import DepartmentRepositoryContract
from schemas import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(self, department_repository: DepartmentRepositoryContract) -> None:
        self.department_repository = department_repository

    def get_all_departments(self) -> list[Department]:
        return self.department_repository.get_all()

    def get_department_by_id(self, department_id: int) -> Department:
        department = self.department_repository.get_by_id(department_id)
        if department is None:
            raise ResourceNotFoundError("Department not found")
        return department

    def create_department(self, department_data: DepartmentCreate) -> Department:
        try:
            return self.department_repository.create(department_data.model_dump())
        except IntegrityError as exc:
            raise ConflictError("Department ID or name already exists") from exc
        except SQLAlchemyError as exc:
            raise DatabaseUnavailableError("Department could not be created because the database is unavailable") from exc

    def update_department(self, department_id: int, department_data: DepartmentUpdate) -> Department:
        department = self.department_repository.get_by_id(department_id)
        if department is None:
            raise ResourceNotFoundError("Department not found")
        payload = department_data.model_dump(exclude_unset=True)
        if not payload:
            raise ValidationError("At least one department field is required for update")
        try:
            return self.department_repository.update(department, payload)
        except IntegrityError as exc:
            raise ConflictError("Department name conflicts with an existing record") from exc
        except SQLAlchemyError as exc:
            raise DatabaseUnavailableError("Department could not be updated because the database is unavailable") from exc

    def delete_department(self, department_id: int) -> None:
        department = self.department_repository.get_by_id(department_id)
        if department is None:
            raise ResourceNotFoundError("Department not found")
        try:
            self.department_repository.delete(department)
        except IntegrityError as exc:
            raise ConflictError("Department cannot be deleted while faculty members are assigned to it") from exc
        except SQLAlchemyError as exc:
            raise DatabaseUnavailableError("Department could not be deleted because the database is unavailable") from exc
