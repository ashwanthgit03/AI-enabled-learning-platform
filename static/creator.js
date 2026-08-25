// Creator / Admin Suite Application Engine (Left Sidebar Layout)
let rolesData = [];
let igotCoursesData = [];
let analyticsChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  loadCreatorRoles();
  loadIGOTCourses();
  loadCreatorEmployees();
  loadAnalytics();
});

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

  if (tabName === 'employees') loadCreatorEmployees();
  if (tabName === 'analytics') loadAnalytics();
  if (tabName === 'igot') loadIGOTCourses();
}

function addCompetencyInputRow() {
  const container = document.getElementById("competencies-container");
  const div = document.createElement("div");
  div.className = "comp-row";
  div.style.display = "flex";
  div.style.gap = "0.5rem";
  div.style.marginBottom = "0.5rem";
  div.innerHTML = `
    <input type="text" class="comp-code" placeholder="Code (e.g. COMP_NAS)" required style="flex: 1; padding: 0.5rem; background: rgba(0,0,0,0.3); border: 1px solid var(--border-light); color: #fff; border-radius: 6px;">
    <input type="text" class="comp-name" placeholder="Competency Name" required style="flex: 2; padding: 0.5rem; background: rgba(0,0,0,0.3); border: 1px solid var(--border-light); color: #fff; border-radius: 6px;">
    <input type="number" class="comp-target" min="1" max="100" placeholder="Target %" required style="width: 90px; padding: 0.5rem; background: rgba(0,0,0,0.3); border: 1px solid var(--border-light); color: #fff; border-radius: 6px;">
  `;
  container.appendChild(div);
}

async function loadCreatorRoles() {
  try {
    const res = await fetch('/api/v1/creator/roles');
    const data = await res.json();
    rolesData = data.roles || [];
    renderCreatorRoleList(rolesData);
    populateCompetencyDropdowns(rolesData);
  } catch (err) {
    console.error("Failed to load roles:", err);
  }
}

function renderCreatorRoleList(roles) {
  const list = document.getElementById("creator-role-list");
  list.innerHTML = '';

  if (roles.length === 0) {
    list.innerHTML = '<p style="color: var(--text-muted);">No roles defined yet.</p>';
    return;
  }

  roles.forEach(r => {
    const card = document.createElement("div");
    card.className = "glass-card";
    card.style.padding = "1rem 1.25rem";
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <h4 style="color: #fff; font-size: 1.05rem;">${r.title}</h4>
        <span style="font-size: 0.75rem; background: rgba(16,185,129,0.15); color: var(--primary); padding: 0.2rem 0.5rem; border-radius: 4px;">${r.department}</span>
      </div>
      <p style="font-size: 0.8rem; color: var(--text-muted); margin: 0.4rem 0;">${r.description}</p>
      <p style="font-size: 0.8rem; color: var(--accent-amber);">Eligibility: ${r.eligibility}</p>
      <div style="margin-top: 0.5rem;">
        ${r.required_competencies.map(c => `
          <span class="competency-tag" style="font-size: 0.75rem;">${c.name} (${c.target_score}%)</span>
        `).join('')}
      </div>
    `;
    list.appendChild(card);
  });
}

function populateCompetencyDropdowns(roles) {
  const dropdownIds = ['igot-comp', 'mat-comp', 'b-q-comp', 'i-q-comp'];
  const compMap = new Map();

  roles.forEach(r => {
    r.required_competencies.forEach(c => {
      compMap.set(c.code, c.name);
    });
  });

  dropdownIds.forEach(id => {
    const select = document.getElementById(id);
    if (!select) return;
    select.innerHTML = '';

    if (compMap.size === 0) {
      select.innerHTML = '<option value="COMP_GOVERNANCE">General Data Governance</option>';
      return;
    }

    compMap.forEach((name, code) => {
      const opt = document.createElement('option');
      opt.value = code;
      opt.innerText = `${name} (${code})`;
      select.appendChild(opt);
    });
  });
}

async function handleCreateRole(e) {
  e.preventDefault();
  const id = document.getElementById("role-id").value.trim();
  const title = document.getElementById("role-title").value.trim();
  const department = document.getElementById("role-dept").value.trim();
  const eligibility = document.getElementById("role-eligibility").value.trim();
  const experience_years = parseInt(document.getElementById("role-exp").value);
  const description = document.getElementById("role-desc").value.trim();

  const compRows = document.querySelectorAll("#competencies-container .comp-row");
  const required_competencies = [];

  compRows.forEach(row => {
    const code = row.querySelector(".comp-code").value.trim();
    const name = row.querySelector(".comp-name").value.trim();
    const target_score = parseFloat(row.querySelector(".comp-target").value);
    if (code && name && target_score) {
      required_competencies.push({ code, name, target_score });
    }
  });

  if (required_competencies.length === 0) {
    alert("Please add at least one required competency target.");
    return;
  }

  const payload = { id, title, department, eligibility, experience_years, description, required_competencies };

  try {
    const res = await fetch("/api/v1/creator/roles", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (res.ok) {
      alert(`🎉 Role '${title}' published successfully to Learner Portal!`);
      document.getElementById("create-role-form").reset();
      loadCreatorRoles();
    } else {
      alert(`Error: ${data.detail}`);
    }
  } catch (err) {
    alert("Failed to publish role.");
  }
}

async function loadIGOTCourses() {
  try {
    const res = await fetch('/api/v1/igot/catalog');
    const data = await res.json();
    igotCoursesData = data.courses || [];
    renderIGOTCourseList(igotCoursesData);
  } catch (err) {
    console.error("Failed to load iGOT catalog:", err);
  }
}

function renderIGOTCourseList(courses) {
  const list = document.getElementById("igot-course-list");
  list.innerHTML = '';

  if (courses.length === 0) {
    list.innerHTML = '<p style="color: var(--text-muted);">No iGOT courses indexed yet.</p>';
    return;
  }

  courses.forEach(c => {
    const card = document.createElement("div");
    card.className = "glass-card";
    card.style.padding = "1rem";
    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <h4 style="color: #fff; font-size: 1rem;">${c.title}</h4>
        <span style="font-size: 0.75rem; background: rgba(6, 182, 212, 0.2); color: var(--accent-cyan); padding: 0.2rem 0.5rem; border-radius: 4px;">${c.competency_code}</span>
      </div>
      <p style="font-size: 0.8rem; color: var(--text-muted); margin: 0.4rem 0;">${c.provider}</p>
      <p style="font-size: 0.8rem; color: var(--text-main); margin-bottom: 0.6rem;">${c.description}</p>
      <a href="${c.igot_url}" target="_blank" style="font-size: 0.75rem; color: var(--accent-cyan); text-decoration: underline;">
        🔗 ${c.igot_url} ↗
      </a>
    `;
    list.appendChild(card);
  });
}

async function handleCreateIGOTCourse(e) {
  e.preventDefault();
  const course_id = document.getElementById("igot-cid").value.trim();
  const title = document.getElementById("igot-title").value.trim();
  const provider = document.getElementById("igot-provider").value.trim();
  const competency_code = document.getElementById("igot-comp").value;
  const igot_url = document.getElementById("igot-url").value.trim();
  const description = document.getElementById("igot-desc").value.trim();

  const payload = { course_id, title, provider, competency_code, igot_url, description };

  try {
    const res = await fetch("/api/v1/creator/igot/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (res.ok) {
      alert(`🎉 iGOT Course '${title}' indexed to database!`);
      document.getElementById("create-igot-course-form").reset();
      loadIGOTCourses();
    } else {
      alert(`Error: ${data.detail}`);
    }
  } catch (err) {
    alert("Failed to index course.");
  }
}

async function triggerLiveScrape() {
  alert("⏳ Scrape request initiated! Fetching live training courses from igotkarmayogi.gov.in...");
  try {
    const res = await fetch('/api/v1/igot/scrape-refresh', { method: 'POST' });
    const data = await res.json();
    alert(`✅ Scrape Complete!\n${data.message}`);
    loadIGOTCourses();
  } catch (err) {
    alert("Scrape failed or timed out.");
  }
}

async function handleUploadMaterial(e) {
  e.preventDefault();
  const title = document.getElementById("mat-title").value.trim();
  const comp = document.getElementById("mat-comp").value;
  const fileInput = document.getElementById("mat-file");

  const formData = new FormData();
  formData.append("title", title);
  formData.append("associated_competency", comp);
  if (fileInput.files[0]) {
    formData.append("file", fileInput.files[0]);
  }

  const status = document.getElementById("upload-status");
  status.innerHTML = '<span style="color: var(--primary);">⏳ Processing document and generating AI evaluation questions...</span>';

  try {
    const res = await fetch("/api/v1/creator/upload-material", {
      method: "POST",
      body: formData
    });
    const data = await res.json();

    if (res.ok) {
      status.innerHTML = `<span style="color: var(--primary);">✅ ${data.message}</span>`;
      document.getElementById("upload-material-form").reset();
    } else {
      status.innerHTML = `<span style="color: var(--accent-rose);">❌ ${data.detail}</span>`;
    }
  } catch (err) {
    status.innerHTML = '<span style="color: var(--accent-rose);">❌ Upload failed.</span>';
  }
}

async function handleCustomQuizSubmit(e, quizType) {
  e.preventDefault();
  const prefix = quizType === 'baseline' ? 'b' : 'i';
  
  const competency_code = document.getElementById(`${prefix}-q-comp`).value;
  const question = document.getElementById(`${prefix}-q-text`).value.trim();

  const optInputs = document.querySelectorAll(`.${prefix}-q-opt`);
  const options = Array.from(optInputs).map(i => i.value.trim());

  const checkedRadio = document.querySelector(`input[name="${prefix}-correct-opt"]:checked`);
  const answer = parseInt(checkedRadio.value);

  const payload = { competency_code, quiz_type: quizType, question, options, answer };

  try {
    const res = await fetch("/api/v1/creator/quiz/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (res.ok) {
      alert(`🎉 Custom ${quizType.toUpperCase()} question saved successfully!`);
      e.target.reset();
    } else {
      alert(`Error: ${data.detail}`);
    }
  } catch (err) {
    alert("Failed to add question.");
  }
}

async function loadCreatorEmployees() {
  try {
    const res = await fetch('/api/v1/creator/employees');
    const data = await res.json();
    const tbody = document.getElementById('creator-employee-tbody');
    tbody.innerHTML = '';

    if (!data.employees || data.employees.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" style="padding: 1rem; color: var(--text-muted); text-align: center;">No government employees registered yet.</td></tr>';
      return;
    }

    data.employees.forEach(emp => {
      const tr = document.createElement('tr');
      tr.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
      const regDate = emp.created_at !== 'N/A' ? new Date(emp.created_at).toLocaleDateString() : 'N/A';

      tr.innerHTML = `
        <td style="padding: 0.75rem;"><code style="color: var(--accent-cyan);">${emp.user_id}</code></td>
        <td style="padding: 0.75rem; font-weight: 600; color: #fff;">${emp.name}</td>
        <td style="padding: 0.75rem; color: var(--text-muted);">${emp.department}</td>
        <td style="padding: 0.75rem; color: var(--accent-amber);">${emp.selected_role_title}</td>
        <td style="padding: 0.75rem;">${emp.enrolled_count} Courses</td>
        <td style="padding: 0.75rem;"><span style="background: rgba(16, 185, 129, 0.2); color: var(--primary); padding: 0.2rem 0.5rem; border-radius: 4px;">🏅 ${emp.badge_count} Badges</span></td>
        <td style="padding: 0.75rem; color: var(--text-muted); font-size: 0.8rem;">${regDate}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Failed to load registered employees:", err);
  }
}

async function loadAnalytics() {
  try {
    const res = await fetch("/api/v1/creator/analytics");
    const data = await res.json();

    document.getElementById("stat-users").innerText = data.total_employees || 0;
    document.getElementById("stat-roles").innerText = data.total_active_roles || 0;
    document.getElementById("stat-docs").innerText = data.total_uploaded_materials || 0;

    const avgs = data.department_competency_averages || {};
    const labels = Object.keys(avgs);
    const scores = Object.values(avgs);

    const ctx = document.getElementById("analyticsChart").getContext("2d");
    if (analyticsChartInstance) {
      analyticsChartInstance.destroy();
    }

    analyticsChartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels.length > 0 ? labels : ["Sampling", "Data Analytics", "Governance"],
        datasets: [{
          label: "Department Average Competency Score (%)",
          data: scores.length > 0 ? scores : [45, 60, 30],
          backgroundColor: "rgba(16, 185, 129, 0.6)",
          borderColor: "#10b981",
          borderWidth: 1,
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { min: 0, max: 100, ticks: { color: "#94a3b8" }, grid: { color: "rgba(255,255,255,0.05)" } },
          x: { ticks: { color: "#f8fafc" }, grid: { display: false } }
        },
        plugins: {
          legend: { labels: { color: "#f8fafc" } }
        }
      }
    });
  } catch (err) {
    console.error("Failed to load analytics:", err);
  }
}
