const state = { faculties: [], departments: [], editingFacultyId: null };

const $ = (selector) => document.querySelector(selector);
const facultyForm = $('#faculty-form');
const departmentForm = $('#department-form');

function showNotice(message, type = 'success') {
  const notice = $('#notice');
  notice.textContent = message;
  notice.className = type;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${response.status})`);
  }
  return response.status === 204 ? null : response.json();
}

function departmentName(id) {
  return state.departments.find((department) => department.department_id === id)?.department_name || `Department ${id}`;
}

function renderDepartmentOptions() {
  const select = $('#department_id');
  select.innerHTML = '<option value="">Select department</option>';
  state.departments.forEach((department) => {
    select.insertAdjacentHTML('beforeend', `<option value="${department.department_id}">${department.department_name}</option>`);
  });
}

function renderDepartments() {
  const body = $('#department-table-body');
  body.innerHTML = state.departments.length
    ? state.departments.map((department) => `
      <tr>
        <td>${department.department_id}</td>
        <td>${department.department_name}</td>
        <td>${department.description || '—'}</td>
        <td class="actions-cell"><button class="table-button delete" data-delete-department="${department.department_id}">Delete</button></td>
      </tr>`).join('')
    : '<tr><td class="empty" colspan="4">No departments found.</td></tr>';
  $('#department-count').textContent = state.departments.length;
}

function renderFaculties() {
  const query = $('#faculty-search').value.toLowerCase();
  const status = $('#status-filter').value;
  const filtered = state.faculties.filter((faculty) => {
    const matchesQuery = [faculty.faculty_id, faculty.full_name, faculty.email, departmentName(faculty.department_id)]
      .some((value) => value.toLowerCase().includes(query));
    return matchesQuery && (!status || faculty.status === status);
  });
  const body = $('#faculty-table-body');
  body.innerHTML = filtered.length
    ? filtered.map((faculty) => `
      <tr>
        <td><strong>${faculty.faculty_id}</strong></td>
        <td>${faculty.full_name}<br><span class="muted">${faculty.email}</span></td>
        <td>${departmentName(faculty.department_id)}</td>
        <td>${faculty.designation}</td>
        <td><span class="badge ${faculty.status === 'On Leave' ? 'leave' : ''}">${faculty.status}</span></td>
        <td class="actions-cell">
          <button class="table-button" data-edit-faculty="${faculty.faculty_id}">Edit</button>
          <button class="table-button delete" data-delete-faculty="${faculty.faculty_id}">Delete</button>
        </td>
      </tr>`).join('')
    : '<tr><td class="empty" colspan="6">No faculty records match your filters.</td></tr>';
  $('#faculty-count').textContent = state.faculties.length;
}

async function loadData() {
  [state.departments, state.faculties] = await Promise.all([
    api('/api/departments'),
    api('/api/faculties'),
  ]);
  renderDepartmentOptions();
  renderDepartments();
  renderFaculties();
}

function resetFacultyForm() {
  facultyForm.reset();
  $('#status').value = 'Active';
  $('#faculty_id').disabled = false;
  state.editingFacultyId = null;
  $('#faculty-submit').textContent = 'Add faculty';
  $('#faculty-cancel').hidden = true;
}

function fillFacultyForm(faculty) {
  state.editingFacultyId = faculty.faculty_id;
  ['faculty_id', 'full_name', 'email', 'phone', 'date_of_birth', 'department_id', 'designation', 'joining_date', 'courses_taught', 'experience_history', 'status']
    .forEach((field) => { $(`#${field}`).value = faculty[field] || ''; });
  $('#faculty_id').disabled = true;
  $('#faculty-submit').textContent = 'Update faculty';
  $('#faculty-cancel').hidden = false;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

facultyForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(facultyForm));
  ['date_of_birth', 'joining_date'].forEach((field) => { if (!data[field]) data[field] = null; });
  data.department_id = Number(data.department_id);
  try {
    if (state.editingFacultyId) {
      await api(`/api/faculties/${state.editingFacultyId}`, { method: 'PUT', body: JSON.stringify(data) });
      showNotice('Faculty record updated.');
    } else {
      await api('/api/faculties', { method: 'POST', body: JSON.stringify(data) });
      showNotice('Faculty record added.');
    }
    resetFacultyForm();
    await loadData();
  } catch (error) { showNotice(error.message, 'error'); }
});

departmentForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const data = Object.fromEntries(new FormData(departmentForm));
  try {
    await api('/api/departments', { method: 'POST', body: JSON.stringify(data) });
    departmentForm.reset();
    await loadData();
    showNotice('Department added.');
  } catch (error) { showNotice(error.message, 'error'); }
});

document.addEventListener('click', async (event) => {
  const editId = event.target.dataset.editFaculty;
  const deleteFacultyId = event.target.dataset.deleteFaculty;
  const deleteDepartmentId = event.target.dataset.deleteDepartment;
  if (editId) fillFacultyForm(state.faculties.find((faculty) => faculty.faculty_id === editId));
  if (deleteFacultyId && confirm(`Delete faculty ${deleteFacultyId}?`)) {
    try { await api(`/api/faculties/${deleteFacultyId}`, { method: 'DELETE' }); await loadData(); showNotice('Faculty deleted.'); }
    catch (error) { showNotice(error.message, 'error'); }
  }
  if (deleteDepartmentId && confirm(`Delete department ${deleteDepartmentId}?`)) {
    try { await api(`/api/departments/${deleteDepartmentId}`, { method: 'DELETE' }); await loadData(); showNotice('Department deleted.'); }
    catch (error) { showNotice(error.message, 'error'); }
  }
});

$('#faculty-cancel').addEventListener('click', resetFacultyForm);
$('#faculty-search').addEventListener('input', renderFaculties);
$('#status-filter').addEventListener('change', renderFaculties);
loadData().catch((error) => showNotice(`Unable to load records: ${error.message}`, 'error'));
