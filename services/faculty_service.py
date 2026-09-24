from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from errors import ConflictError, DatabaseUnavailableError, ResourceNotFoundError, ValidationError
from models import Faculty
from repositories.contracts import DepartmentRepositoryContract, FacultyRepositoryContract
from schemas import FacultyCreate, FacultyUpdate


class FacultyService:
    def __init__(self, faculty_repository: FacultyRepositoryContract, department_repository: DepartmentRepositoryContract) -> None:
        self.faculty_repository = faculty_repository
        self.department_repository = department_repository

    def get_all_faculties(self) -> list[Faculty]:
        return self.faculty_repository.get_all()

    def get_faculty_by_id(self, faculty_id: str) -> Faculty:
        faculty = self.faculty_repository.get_by_id(faculty_id)
        if faculty is None:
            raise ResourceNotFoundError("Faculty not found")
        return faculty

    def create_faculty(self, faculty_data: FacultyCreate) -> Faculty:
        payload = faculty_data.model_dump()
        if self.department_repository.get_by_id(payload["department_id"]) is None:
            raise ValidationError("The specified department does not exist")
        try:
            return self.faculty_repository.create(payload)
        except IntegrityError as exc:
            raise ConflictError("Faculty ID, email, or department relationship conflicts with an existing record") from exc
        except SQLAlchemyError as exc:
            raise DatabaseUnavailableError("Faculty could not be created because the database is unavailable") from exc

    def update_faculty(self, faculty_id: str, faculty_data: FacultyUpdate) -> Faculty:
        faculty = self.faculty_repository.get_by_id(faculty_id)
        if faculty is None:
            raise ResourceNotFoundError("Faculty not found")
        payload = faculty_data.model_dump(exclude_unset=True)
        if not payload:
            raise ValidationError("At least one faculty field is required for update")
        if "department_id" in payload and self.department_repository.get_by_id(payload["department_id"]) is None:
            raise ValidationError("The specified department does not exist")
        try:
            return self.faculty_repository.update(faculty, payload)
        except IntegrityError as exc:
            raise ConflictError("Faculty email or department relationship conflicts with an existing record") from exc
        except SQLAlchemyError as exc:
            raise DatabaseUnavailableError("Faculty could not be updated because the database is unavailable") from exc

    def delete_faculty(self, faculty_id: str) -> None:
        faculty = self.faculty_repository.get_by_id(faculty_id)
        if faculty is None:
            raise ResourceNotFoundError("Faculty not found")
        try:
            self.faculty_repository.delete(faculty)
        except SQLAlchemyError as exc:
            raise DatabaseUnavailableError("Faculty could not be deleted because the database is unavailable") from exc
