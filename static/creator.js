// Creator & Admin Control Center Logic Engine
let creatorRoles = [];
let creatorCourses = [];
let analyticsChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  loadCreatorRoles();
  loadCreatorCourses();
  loadCompetencyOptions();
  loadCreatorEmployees();
  loadCreatorAnalytics();
});

// Fancy Glassmorphic Popup Modal Engine
function showFancyPopup(title, message, type = 'success', onClose = null) {
  const container = document.getElementById('fancy-modal-container');
  if (!container) return;

  const icon = type === 'success' ? '🎉' : (type === 'error' ? '❌' : 'ℹ️');
  const borderColor = type === 'success' ? '#a7f3d0' : (type === 'error' ? '#fca5a5' : '#bfdbfe');
  const titleColor = type === 'success' ? '#16a34a' : (type === 'error' ? '#dc2626' : '#2563eb');

  container.className = 'fancy-modal-overlay';
  container.innerHTML = `
    <div class="fancy-modal-box" style="border: 2px solid ${borderColor};">
      <div style="font-size: 3rem; margin-bottom: 0.5rem;">${icon}</div>
      <h3 style="color: ${titleColor}; font-size: 1.4rem; margin-bottom: 0.6rem;">${title}</h3>
      <p style="color: #475569; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">${message}</p>
      <button class="btn btn-primary" style="padding: 0.75rem 2rem; border-radius: 12px; justify-content: center; width: 100%;" onclick="closeFancyPopup()">OK, Continue</button>
    </div>
  `;

  window._fancyOnClose = onClose;
}

function closeFancyPopup() {
  const container = document.getElementById('fancy-modal-container');
  if (container) {
    container.className = 'hidden';
    container.innerHTML = '';
  }
  if (typeof window._fancyOnClose === 'function') {
    window._fancyOnClose();
    window._fancyOnClose = null;
  }
}

function refreshAllCreatorData() {
  loadCreatorRoles();
  loadCreatorCourses();
  loadCompetencyOptions();
  loadCreatorEmployees();
  loadCreatorAnalytics();
  showFancyPopup("Database Refreshed", "All registries and roles refreshed successfully.", "success");
}

function switchCreatorTab(tabName) {
  const tabs = ['roles', 'igot', 'upload', 'baseline-quiz', 'intermediate-quiz', 'employees', 'analytics'];
  tabs.forEach(t => {
    const btn = document.getElementById(`tab-btn-${t}`);
    const content = document.getElementById(`tab-content-${t}`);
    if (btn && content) {
      if (t === tabName) {
        btn.classList.add('active');
        content.classList.remove('hidden');
      } else {
        btn.classList.remove('active');
        content.classList.add('hidden');
      }
    }
  });

  if (tabName === 'analytics') loadCreatorAnalytics();
  if (tabName === 'employees') loadCreatorEmployees();
}

async function loadCreatorRoles() {
  try {
    const res = await fetch('/api/v1/creator/roles');
    const data = await res.json();
    creatorRoles = data.roles || [];
    renderCreatorRoles(creatorRoles);
    loadCompetencyOptions();
  } catch (err) {
    console.error("Failed to load roles:", err);
  }
}

function renderCreatorRoles(roles) {
  const container = document.getElementById('creator-role-list');
  container.innerHTML = '';

  if (roles.length === 0) {
    container.innerHTML = '<p style="color: var(--text-muted);">No government roles created yet.</p>';
    return;
  }

  roles.forEach(role => {
    const card = document.createElement('div');
    card.className = 'glass-card';
    card.style.padding = '1.2rem';

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <h4 style="color: #172033; font-size: 1.1rem;">${role.title}</h4>
          <span style="font-size: 0.75rem; color: var(--primary); background: #eff6ff; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700;">${role.department}</span>
        </div>
        <button class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.3rem 0.6rem;" onclick="openEditRoleModal('${role.id}')">
          ✏️ Edit & Modify Benchmarks
        </button>
      </div>

      <p style="font-size: 0.85rem; color: var(--text-muted); margin: 0.5rem 0;">${role.description}</p>
      
      <div style="margin-top: 0.5rem;">
        <strong style="font-size: 0.8rem; color: var(--accent-amber); display: block; margin-bottom: 0.3rem;">Target Competency Benchmarks:</strong>
        ${role.required_competencies.map(c => `
          <span class="competency-tag">${c.name} (${c.target_score}%)</span>
        `).join('')}
      </div>
    `;
    container.appendChild(card);
  });
}

function addCompetencyInputRow() {
  const container = document.getElementById('competencies-container');
  const div = document.createElement('div');
  div.className = 'comp-row';
  div.style.display = 'flex';
  div.style.gap = '0.5rem';
  div.style.marginBottom = '0.5rem';

  div.innerHTML = `
    <input type="text" class="comp-code" placeholder="Competency Code" required style="flex: 1; padding: 0.5rem 0.75rem; background: #f8fafc; border: 1px solid #dbe2ea; color: #172033; border-radius: 6px;">
    <input type="text" class="comp-name" placeholder="Competency Name" required style="flex: 2; padding: 0.5rem 0.75rem; background: #f8fafc; border: 1px solid #dbe2ea; color: #172033; border-radius: 6px;">
    <input type="number" class="comp-target" min="1" max="100" placeholder="Target %" required style="width: 90px; padding: 0.5rem 0.75rem; background: #f8fafc; border: 1px solid #dbe2ea; color: #172033; border-radius: 6px;">
    <button type="button" onclick="this.parentElement.remove()" style="background: none; border: none; color: red; cursor: pointer; font-weight: bold;">✕</button>
  `;
  container.appendChild(div);
}

async function handleCreateRole(e) {
  e.preventDefault();
  
  const compRows = document.querySelectorAll('#competencies-container .comp-row');
  const requiredCompetencies = [];

  compRows.forEach(row => {
    const code = row.querySelector('.comp-code').value.trim();
    const name = row.querySelector('.comp-name').value.trim();
    const target = parseFloat(row.querySelector('.comp-target').value);
    if (code && name && !isNaN(target)) {
      requiredCompetencies.push({ code, name, target_score: target });
    }
  });

  const payload = {
    id: document.getElementById('role-id').value.trim(),
    title: document.getElementById('role-title').value.trim(),
    department: document.getElementById('role-dept').value.trim(),
    eligibility: document.getElementById('role-eligibility').value.trim(),
    experience_years: parseInt(document.getElementById('role-exp').value),
    description: document.getElementById('role-desc').value.trim(),
    required_competencies: requiredCompetencies
  };

  try {
    const res = await fetch('/api/v1/creator/roles', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (res.ok) {
      showFancyPopup("Role Created", data.message, "success");
      document.getElementById('create-role-form').reset();
      loadCreatorRoles();
    } else {
      showFancyPopup("Error Creating Role", data.detail, "error");
    }
  } catch (err) {
    showFancyPopup("Error", "Failed to communicate with server.", "error");
  }
}

// EDIT ROLE MODAL LOGIC
function openEditRoleModal(roleId) {
  const role = creatorRoles.find(r => r.id === roleId);
  if (!role) return;

  document.getElementById('edit-role-id').value = role.id;
  document.getElementById('edit-role-title').value = role.title;
  document.getElementById('edit-role-dept').value = role.department;
  document.getElementById('edit-role-eligibility').value = role.eligibility;

  const container = document.getElementById('edit-competencies-container');
  container.innerHTML = '';

  role.required_competencies.forEach(comp => {
    const div = document.createElement('div');
    div.className = 'edit-comp-row';
    div.style.display = 'flex';
    div.style.gap = '0.5rem';

    div.innerHTML = `
      <input type="text" class="edit-comp-code" value="${comp.code}" placeholder="Code" required style="flex: 1; padding: 0.5rem; background: #f8fafc; border: 1px solid #dbe2ea; border-radius: 6px;">
      <input type="text" class="edit-comp-name" value="${comp.name}" placeholder="Name" required style="flex: 2; padding: 0.5rem; background: #f8fafc; border: 1px solid #dbe2ea; border-radius: 6px;">
      <input type="number" class="edit-comp-target" min="1" max="100" value="${comp.target_score}" placeholder="Target %" required style="width: 90px; padding: 0.5rem; background: #f8fafc; border: 1px solid #dbe2ea; border-radius: 6px;">
      <button type="button" onclick="this.parentElement.remove()" style="background: none; border: none; color: red; cursor: pointer; font-weight: bold;">✕</button>
    `;
    container.appendChild(div);
  });

  document.getElementById('edit-role-modal').classList.remove('hidden');
}

function closeEditRoleModal() {
  document.getElementById('edit-role-modal').classList.add('hidden');
}

function addEditCompetencyRow() {
  const container = document.getElementById('edit-competencies-container');
  const div = document.createElement('div');
  div.className = 'edit-comp-row';
  div.style.display = 'flex';
  div.style.gap = '0.5rem';

  div.innerHTML = `
    <input type="text" class="edit-comp-code" placeholder="Code" required style="flex: 1; padding: 0.5rem; background: #f8fafc; border: 1px solid #dbe2ea; border-radius: 6px;">
    <input type="text" class="edit-comp-name" placeholder="Name" required style="flex: 2; padding: 0.5rem; background: #f8fafc; border: 1px solid #dbe2ea; border-radius: 6px;">
    <input type="number" class="edit-comp-target" min="1" max="100" placeholder="Target %" required style="width: 90px; padding: 0.5rem; background: #f8fafc; border: 1px solid #dbe2ea; border-radius: 6px;">
    <button type="button" onclick="this.parentElement.remove()" style="background: none; border: none; color: red; cursor: pointer; font-weight: bold;">✕</button>
  `;
  container.appendChild(div);
}

async function handleSaveRoleEdit(e) {
  e.preventDefault();
  const roleId = document.getElementById('edit-role-id').value;

  const compRows = document.querySelectorAll('#edit-competencies-container .edit-comp-row');
  const requiredCompetencies = [];

  compRows.forEach(row => {
    const code = row.querySelector('.edit-comp-code').value.trim();
    const name = row.querySelector('.edit-comp-name').value.trim();
    const target = parseFloat(row.querySelector('.edit-comp-target').value);
    if (code && name && !isNaN(target)) {
      requiredCompetencies.push({ code, name, target_score: target });
    }
  });

  const payload = {
    title: document.getElementById('edit-role-title').value.trim(),
    department: document.getElementById('edit-role-dept').value.trim(),
    eligibility: document.getElementById('edit-role-eligibility').value.trim(),
    required_competencies: requiredCompetencies
  };

  try {
    const res = await fetch(`/api/v1/creator/roles/${roleId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (res.ok) {
      closeEditRoleModal();
      showFancyPopup("Role Updated", data.message, "success");
      loadCreatorRoles();
    } else {
      showFancyPopup("Update Error", data.detail, "error");
    }
  } catch (err) {
    showFancyPopup("Error", "Failed to update role.", "error");
  }
}

async function loadCreatorCourses() {
  try {
    const res = await fetch('/api/v1/igot/catalog');
    const data = await res.json();
    creatorCourses = data.courses || [];
    renderCreatorCourses(creatorCourses);
  } catch (err) {
    console.error("Failed to load iGOT catalog:", err);
  }
}

function renderCreatorCourses(courses) {
  const container = document.getElementById('igot-course-list');
  container.innerHTML = '';

  if (courses.length === 0) {
    container.innerHTML = '<p style="color: var(--text-muted);">No iGOT courses indexed.</p>';
    return;
  }

  courses.forEach(c => {
    const card = document.createElement('div');
    card.className = 'glass-card';
    card.style.padding = '1rem';

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <h4 style="color: #172033; font-size: 1rem;">${c.title}</h4>
        <span style="font-size: 0.75rem; background: #ecfdf5; color: var(--accent-green); padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700;">${c.competency_code}</span>
      </div>
      <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.3rem;">${c.provider}</p>
      <a href="${c.igot_url}" target="_blank" style="font-size: 0.8rem; color: var(--primary); display: inline-block; margin-top: 0.5rem;">🔗 View Direct iGOT Course Link ↗</a>
    `;
    container.appendChild(card);
  });
}

function loadCompetencyOptions() {
  const compSet = new Set();
  creatorRoles.forEach(r => {
    r.required_competencies.forEach(c => compSet.add(c.code));
  });

  const selectors = ['igot-comp', 'mat-comp', 'b-q-comp', 'i-q-comp'];
  selectors.forEach(sId => {
    const select = document.getElementById(sId);
    if (!select) return;
    select.innerHTML = '';
    compSet.forEach(code => {
      const opt = document.createElement('option');
      opt.value = code;
      opt.innerText = code;
      select.appendChild(opt);
    });
  });
}

async function handleCreateIGOTCourse(e) {
  e.preventDefault();
  const payload = {
    course_id: document.getElementById('igot-cid').value.trim(),
    title: document.getElementById('igot-title').value.trim(),
    provider: document.getElementById('igot-provider').value.trim(),
    competency_code: document.getElementById('igot-comp').value,
    igot_url: document.getElementById('igot-url').value.trim(),
    description: document.getElementById('igot-desc').value.trim()
  };

  try {
    const res = await fetch('/api/v1/creator/igot/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok) {
      showFancyPopup("Course Indexed", data.message, "success");
      document.getElementById('create-igot-course-form').reset();
      loadCreatorCourses();
    } else {
      showFancyPopup("Error", data.detail, "error");
    }
  } catch (err) {
    showFancyPopup("Error", "Failed to add course.", "error");
  }
}

async function triggerLiveScrape() {
  try {
    const res = await fetch('/api/v1/igot/scrape-refresh', { method: 'POST' });
    const data = await res.json();
    showFancyPopup("Scraper Finished", data.message, "success");
    loadCreatorCourses();
  } catch (err) {
    showFancyPopup("Error", "Failed to trigger live scraper.", "error");
  }
}

async function handleUploadMaterial(e) {
  e.preventDefault();
  const title = document.getElementById('mat-title').value.trim();
  const comp = document.getElementById('mat-comp').value;
  const fileInput = document.getElementById('mat-file');

  const formData = new FormData();
  formData.append('title', title);
  formData.append('associated_competency', comp);
  if (fileInput.files.length > 0) {
    formData.append('file', fileInput.files[0]);
  }

  const statusDiv = document.getElementById('upload-status');
  statusDiv.innerHTML = '<span style="color: var(--primary);">⏳ Ingesting document & generating RAG MCQs...</span>';

  try {
    const res = await fetch('/api/v1/creator/upload-material', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    if (res.ok) {
      statusDiv.innerHTML = `<span style="color: var(--accent-green);">✅ ${data.message}</span>`;
      showFancyPopup("PDF Ingestion & RAG Complete", data.message, "success");
      document.getElementById('upload-material-form').reset();
    } else {
      statusDiv.innerHTML = `<span style="color: var(--accent-red);">❌ ${data.detail}</span>`;
    }
  } catch (err) {
    statusDiv.innerHTML = '<span style="color: var(--accent-red);">❌ Upload failed.</span>';
  }
}

async function handleCustomQuizSubmit(e, type) {
  e.preventDefault();
  const compCode = document.getElementById(type === 'baseline' ? 'b-q-comp' : 'i-q-comp').value;
  const question = document.getElementById(type === 'baseline' ? 'b-q-text' : 'i-q-text').value.trim();
  
  const optInputs = document.querySelectorAll(type === 'baseline' ? '.b-q-opt' : '.i-q-opt');
  const options = Array.from(optInputs).map(inp => inp.value.trim());

  const radios = document.getElementsByName(type === 'baseline' ? 'b-correct-opt' : 'i-correct-opt');
  let answer = 0;
  radios.forEach(r => { if (r.checked) answer = parseInt(r.value); });

  const payload = {
    competency_code: compCode,
    quiz_type: type,
    question: question,
    options: options,
    answer: answer
  };

  try {
    const res = await fetch('/api/v1/creator/quiz/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok) {
      showFancyPopup("Quiz Question Saved", data.message, "success");
      e.target.reset();
    } else {
      showFancyPopup("Error", data.detail, "error");
    }
  } catch (err) {
    showFancyPopup("Error", "Failed to save question.", "error");
  }
}

async function loadCreatorEmployees() {
  try {
    const res = await fetch('/api/v1/creator/employees');
    const data = await res.json();
    renderCreatorEmployeeTable(data.employees || []);
  } catch (err) {
    console.error("Failed to load registered employees:", err);
  }
}

function renderCreatorEmployeeTable(employees) {
  const tbody = document.getElementById('creator-employee-tbody');
  tbody.innerHTML = '';

  if (employees.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" style="padding: 1.5rem; text-align: center; color: var(--text-muted);">No government officers registered yet.</td></tr>';
    return;
  }

  employees.forEach(emp => {
    const tr = document.createElement('tr');
    tr.style.borderBottom = '1px solid var(--border-light)';

    tr.innerHTML = `
      <td style="padding: 0.75rem; font-weight: 700; color: var(--primary);">${emp.user_id}</td>
      <td style="padding: 0.75rem; font-weight: 600; color: #172033;">${emp.name}</td>
      <td style="padding: 0.75rem; color: var(--text-muted);">${emp.department}</td>
      <td style="padding: 0.75rem; color: var(--accent-amber); font-weight: 600;">${emp.selected_role_title}</td>
      <td style="padding: 0.75rem;">${emp.enrolled_count} courses</td>
      <td style="padding: 0.75rem;">🏅 ${emp.badge_count} badges</td>
      <td style="padding: 0.75rem;">
        <button class="btn btn-danger" style="padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="deleteEmployee('${emp.user_id}', '${emp.name.replace(/'/g, "\\'")}')">
          🗑️ Revoke Access
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function deleteEmployee(userId, name) {
  if (!confirm(`Are you sure you want to revoke access and delete account for Officer ${name} (${userId})?`)) return;

  try {
    const res = await fetch(`/api/v1/creator/employee/${userId}`, { method: 'DELETE' });
    const data = await res.json();
    if (res.ok) {
      showFancyPopup("Access Revoked", data.message, "success");
      loadCreatorEmployees();
    } else {
      showFancyPopup("Error", data.detail, "error");
    }
  } catch (err) {
    showFancyPopup("Error", "Failed to delete employee account.", "error");
  }
}

async function loadCreatorAnalytics() {
  try {
    const res = await fetch('/api/v1/creator/analytics');
    const data = await res.json();

    document.getElementById('stat-users').innerText = data.total_employees;
    document.getElementById('stat-roles').innerText = data.total_active_roles;
    document.getElementById('stat-docs').innerText = data.total_uploaded_materials;

    renderAnalyticsChart(data.department_competency_averages);
  } catch (err) {
    console.error("Failed to load analytics:", err);
  }
}

function renderAnalyticsChart(averages) {
  const labels = Object.keys(averages);
  const values = Object.values(averages);

  const ctx = document.getElementById('analyticsChart').getContext('2d');
  if (analyticsChartInstance) {
    analyticsChartInstance.destroy();
  }

  analyticsChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels.length ? labels : ['COMP_GOVERNANCE', 'COMP_FINANCE', 'COMP_DATA_ANALYTICS'],
      datasets: [{
        label: 'Average Employee Benchmark Score (%)',
        data: values.length ? values : [75, 60, 85],
        backgroundColor: 'rgba(37, 99, 235, 0.65)',
        borderColor: '#2563eb',
        borderWidth: 2,
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { min: 0, max: 100, ticks: { color: '#64748b' } },
        x: { ticks: { color: '#172033', font: { weight: '700' } } }
      }
    }
  });
}
