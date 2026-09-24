from unittest.mock import Mock

import pytest

from errors import ResourceNotFoundError, ValidationError
from schemas import DepartmentCreate, DepartmentUpdate
from services.department_service import DepartmentService


def build_service(repository=None):
    return DepartmentService(repository or Mock())


def test_get_all_departments_returns_repository_records(department_record):
    repository = Mock(); repository.get_all.return_value = [department_record]
    assert build_service(repository).get_all_departments() == [department_record]
    repository.get_all.assert_called_once_with()


def test_get_department_by_id_raises_when_missing():
    repository = Mock(); repository.get_by_id.return_value = None
    with pytest.raises(ResourceNotFoundError, match="Department not found"):
        build_service(repository).get_department_by_id(404)


def test_create_department_persists_valid_data(department_record):
    repository = Mock(); repository.create.return_value = department_record
    result = build_service(repository).create_department(DepartmentCreate(department_id=1, department_name="Computer Science and Engineering", description="Computing department"))
    assert result == department_record
    repository.create.assert_called_once()


def test_update_department_rejects_empty_payload(department_record):
    repository = Mock(); repository.get_by_id.return_value = department_record
    with pytest.raises(ValidationError, match="At least one department field"):
        build_service(repository).update_department(1, DepartmentUpdate())


def test_delete_department_deletes_existing_record(department_record):
    repository = Mock(); repository.get_by_id.return_value = department_record
    build_service(repository).delete_department(1)
    repository.delete.assert_called_once_with(department_record)
