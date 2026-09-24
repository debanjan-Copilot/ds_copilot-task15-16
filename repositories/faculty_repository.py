from collections.abc import Mapping

from models import Faculty
from repositories.base_repository import BaseRepository


class FacultyRepository(BaseRepository):
    def get_all(self) -> list[Faculty]:
        return self.db.query(Faculty).order_by(Faculty.faculty_id.asc()).all()

    def get_by_id(self, faculty_id: str) -> Faculty | None:
        return self.db.query(Faculty).filter(Faculty.faculty_id == faculty_id).first()

    def create(self, faculty_data: Mapping[str, object]) -> Faculty:
        return self.save(Faculty(**faculty_data))

    def update(self, faculty: Faculty, faculty_data: Mapping[str, object]) -> Faculty:
        for key, value in faculty_data.items():
            if value is not None:
                setattr(faculty, key, value)
        self.commit()
        return self.refresh(faculty)

    def delete(self, faculty: Faculty) -> None:
        super().delete(faculty)
