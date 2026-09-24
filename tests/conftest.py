from types import SimpleNamespace

import pytest


@pytest.fixture
def faculty_record():
    return SimpleNamespace(faculty_id="FAC101", full_name="Dr. Eleanor Vance", department_id=1, email="eleanor.vance@university.edu")


@pytest.fixture
def department_record():
    return SimpleNamespace(department_id=1, department_name="Computer Science and Engineering")
