from unittest.mock import Mock

from controllers import department_controller, faculty_controller
from schemas import DepartmentCreate, DepartmentUpdate, FacultyCreate, FacultyUpdate


def test_faculty_controller_get_all_delegates_to_service(faculty_record):
    service = Mock(); service.get_all_faculties.return_value = [faculty_record]
    assert faculty_controller.get_faculties(service) == [faculty_record]
    service.get_all_faculties.assert_called_once_with()


def test_faculty_controller_create_delegates_to_service():
    service = Mock(); payload = Mock(spec=FacultyCreate); service.create_faculty.return_value = "created"
    assert faculty_controller.create_faculty(payload, service) == "created"
    service.create_faculty.assert_called_once_with(payload)


def test_faculty_controller_update_and_delete_delegate():
    service = Mock(); payload = Mock(spec=FacultyUpdate); service.update_faculty.return_value = "updated"
    assert faculty_controller.update_faculty("FAC101", payload, service) == "updated"
    faculty_controller.delete_faculty("FAC101", service)
    service.update_faculty.assert_called_once_with("FAC101", payload)
    service.delete_faculty.assert_called_once_with("FAC101")


def test_department_controller_get_and_create_delegate(department_record):
    service = Mock(); service.get_department_by_id.return_value = department_record; service.create_department.return_value = "created"
    payload = Mock(spec=DepartmentCreate)
    assert department_controller.get_department(1, service) == department_record
    assert department_controller.create_department(payload, service) == "created"
    service.get_department_by_id.assert_called_once_with(1)
    service.create_department.assert_called_once_with(payload)


def test_department_controller_update_and_delete_delegate():
    service = Mock(); payload = Mock(spec=DepartmentUpdate); service.update_department.return_value = "updated"
    assert department_controller.update_department(1, payload, service) == "updated"
    department_controller.delete_department(1, service)
    service.update_department.assert_called_once_with(1, payload)
    service.delete_department.assert_called_once_with(1)
