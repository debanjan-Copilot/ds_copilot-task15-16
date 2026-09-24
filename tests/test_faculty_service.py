from datetime import date
from unittest.mock import Mock

import pytest

from errors import ResourceNotFoundError, ValidationError
from schemas import FacultyCreate, FacultyUpdate
from services.faculty_service import FacultyService


def create_faculty_payload() -> FacultyCreate:
    return FacultyCreate(faculty_id="FAC101", full_name="Dr. Eleanor Vance", email="eleanor.vance@university.edu", phone="+1-555-0142", date_of_birth=date(1978, 4, 15), department_id=1, designation="Professor", joining_date=date(2010, 8, 1), courses_taught="Algorithms", experience_history="Postdoc at MIT", status="Active")


def build_service(faculty_repository=None, department_repository=None):
    return FacultyService(faculty_repository or Mock(), department_repository or Mock())


def test_get_all_faculties_returns_repository_records(faculty_record):
    repository = Mock(); repository.get_all.return_value = [faculty_record]
    assert build_service(faculty_repository=repository).get_all_faculties() == [faculty_record]
    repository.get_all.assert_called_once_with()


def test_get_faculty_by_id_raises_when_missing():
    repository = Mock(); repository.get_by_id.return_value = None
    with pytest.raises(ResourceNotFoundError, match="Faculty not found"):
        build_service(faculty_repository=repository).get_faculty_by_id("FAC404")


def test_create_faculty_validates_department_and_persists(faculty_record, department_record):
    faculty_repository = Mock(); faculty_repository.create.return_value = faculty_record
    department_repository = Mock(); department_repository.get_by_id.return_value = department_record
    assert build_service(faculty_repository, department_repository).create_faculty(create_faculty_payload()) == faculty_record
    department_repository.get_by_id.assert_called_once_with(1)
    faculty_repository.create.assert_called_once()


def test_create_faculty_rejects_unknown_department():
    department_repository = Mock(); department_repository.get_by_id.return_value = None
    faculty_repository = Mock()
    with pytest.raises(ValidationError, match="department does not exist"):
        build_service(faculty_repository, department_repository).create_faculty(create_faculty_payload())
    faculty_repository.create.assert_not_called()


def test_update_faculty_rejects_empty_payload(faculty_record):
    repository = Mock(); repository.get_by_id.return_value = faculty_record
    with pytest.raises(ValidationError, match="At least one faculty field"):
        build_service(faculty_repository=repository).update_faculty("FAC101", FacultyUpdate())


def test_delete_faculty_deletes_existing_record(faculty_record):
    repository = Mock(); repository.get_by_id.return_value = faculty_record
    service = build_service(faculty_repository=repository); service.delete_faculty("FAC101")
    repository.delete.assert_called_once_with(faculty_record)
