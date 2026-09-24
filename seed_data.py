from datetime import datetime

from database import Base, SessionLocal, engine
from models import Department, Faculty


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        departments = [
            Department(department_id=1, department_name="Computer Science and Engineering", description="Focuses on computation, algorithms, software development, and artificial intelligence."),
            Department(department_id=2, department_name="Mathematics", description="Covers pure and applied mathematics, statistics, and advanced mathematical modeling."),
            Department(department_id=3, department_name="Physics", description="Explores the fundamental laws of nature, quantum mechanics, and physical systems."),
        ]
        if db.query(Department).count() == 0:
            db.add_all(departments)
            db.commit()
        if db.query(Faculty).count() == 0:
            timestamp = datetime.strptime("2026-01-10 09:00:00", "%Y-%m-%d %H:%M:%S")
            db.add_all([
                Faculty(faculty_id="FAC101", full_name="Dr. Eleanor Vance", email="eleanor.vance@university.edu", department_id=1, designation="Professor", status="Active", created_at=timestamp, updated_at=timestamp),
                Faculty(faculty_id="FAC102", full_name="Dr. Marcus Chen", email="marcus.chen@university.edu", department_id=2, designation="Associate Professor", status="Active", created_at=timestamp, updated_at=timestamp),
                Faculty(faculty_id="FAC103", full_name="Prof. Sarah Jenkins", email="sarah.jenkins@university.edu", department_id=3, designation="Assistant Professor", status="On Leave", created_at=timestamp, updated_at=timestamp),
            ])
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
