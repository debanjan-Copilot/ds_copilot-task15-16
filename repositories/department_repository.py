from collections.abc import Mapping

from models import Department
from repositories.base_repository import BaseRepository


class DepartmentRepository(BaseRepository):
    def get_all(self) -> list[Department]:
        return self.db.query(Department).order_by(Department.department_id.asc()).all()

    def get_by_id(self, department_id: int) -> Department | None:
        return self.db.query(Department).filter(Department.department_id == department_id).first()

    def create(self, department_data: Mapping[str, object]) -> Department:
        return self.save(Department(**department_data))

    def update(self, department: Department, department_data: Mapping[str, object]) -> Department:
        for key, value in department_data.items():
            if value is not None:
                setattr(department, key, value)
        self.commit()
        return self.refresh(department)

    def delete(self, department: Department) -> None:
        super().delete(department)
