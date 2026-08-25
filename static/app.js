// Learner Portal Interactive Application Logic & Authentication Engine
let activeUser = null;
let currentUserId = null;
let selectedRoleId = null;
let allLearnerRoles = [];

let activeBaselineQuestions = [];
let activeIntermediateQuestions = [];
let selectedBaselineAnswers = {};
let selectedIntermediateAnswers = {};
let currentActiveCompForIntQuiz = null;

let gapRadarChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
  checkAuthSession();
});

function checkAuthSession() {
  const savedUser = localStorage.getItem("mospi_active_user");
  if (savedUser) {
    try {
      activeUser = JSON.parse(savedUser);
      currentUserId = activeUser.user_id;
      
      document.getElementById('auth-modal').classList.add('hidden');
      document.getElementById('nav-officer-info').innerText = `${activeUser.name} (${activeUser.user_id})`;
      
      loadLearnerRoles();
      loadLiveUserProfile();
    } catch (e) {
      showAuthModal();
    }
  } else {
    showAuthModal();
  }
}

function showAuthModal() {
  document.getElementById('auth-modal').classList.remove('hidden');
}

function switchAuthTab(mode) {
  const loginForm = document.getElementById('login-form');
  const regForm = document.getElementById('register-form');
  const btnLogin = document.getElementById('tab-auth-login');
  const btnReg = document.getElementById('tab-auth-register');
  const title = document.getElementById('auth-modal-title');
  const subtitle = document.getElementById('auth-modal-subtitle');
  const errMsg = document.getElementById('auth-error-msg');

  errMsg.innerText = '';

  if (mode === 'login') {
    loginForm.classList.remove('hidden');
    regForm.classList.add('hidden');
    btnLogin.className = 'btn btn-primary';
    btnReg.className = 'btn btn-secondary';
    title.innerText = "Government Officer Login";
    subtitle.innerText = "Sign in to continue your competency learning journey";
  } else {
    loginForm.classList.add('hidden');
    regForm.classList.remove('hidden');
    btnLogin.className = 'btn btn-secondary';
    btnReg.className = 'btn btn-success';
    title.innerText = "Register New Government Officer";
    subtitle.innerText = "Account info will be saved permanently in Creator Portal";
  }
}

async function handleLoginSubmit(e) {
  e.preventDefault();
  const uid = document.getElementById('login-user-id').value.trim();
  const pass = document.getElementById('login-password').value;
  const errMsg = document.getElementById('auth-error-msg');

  errMsg.innerHTML = '<span style="color: var(--primary);">⏳ Authenticating...</span>';

  try {
    const res = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: uid, password: pass })
    });
    const data = await res.json();

    if (res.ok) {
      activeUser = data.user;
      currentUserId = activeUser.user_id;
      localStorage.setItem("mospi_active_user", JSON.stringify(activeUser));
      
      document.getElementById('auth-modal').classList.add('hidden');
      document.getElementById('nav-officer-info').innerText = `${activeUser.name} (${activeUser.user_id})`;
      
      loadLearnerRoles();
      loadLiveUserProfile();
    } else {
      errMsg.innerHTML = `<span style="color: var(--accent-red);">❌ ${data.detail}</span>`;
    }
  } catch (err) {
    errMsg.innerHTML = '<span style="color: var(--accent-red);">❌ Network error during login.</span>';
  }
}

async function handleRegisterSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('reg-name').value.trim();
  const uid = document.getElementById('reg-user-id').value.trim();
  const dept = document.getElementById('reg-dept').value.trim();
  const pass = document.getElementById('reg-password').value;
  const errMsg = document.getElementById('auth-error-msg');

  errMsg.innerHTML = '<span style="color: var(--primary);">⏳ Creating account...</span>';

  try {
    const res = await fetch('/api/v1/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: uid, name: name, department: dept, password: pass })
    });
    const data = await res.json();

    if (res.ok) {
      alert(`🎉 Registration Successful!\nAccount created for ${data.user.name} (${data.user.user_id}). Saved to Creator Portal.`);
      activeUser = data.user;
      currentUserId = activeUser.user_id;
      localStorage.setItem("mospi_active_user", JSON.stringify(activeUser));

      document.getElementById('auth-modal').classList.add('hidden');
      document.getElementById('nav-officer-info').innerText = `${activeUser.name} (${activeUser.user_id})`;

      loadLearnerRoles();
      loadLiveUserProfile();
    } else {
      errMsg.innerHTML = `<span style="color: var(--accent-red);">❌ ${data.detail}</span>`;
    }
  } catch (err) {
    errMsg.innerHTML = '<span style="color: var(--accent-red);">❌ Registration failed.</span>';
  }
}

function handleLogout() {
  localStorage.removeItem("mospi_active_user");
  activeUser = null;
  currentUserId = null;
  selectedRoleId = null;
  document.getElementById('nav-officer-info').innerText = "Not Logged In";
  showAuthModal();
}

function switchStep(stepNumber) {
  for (let i = 1; i <= 5; i++) {
    const navItem = document.getElementById(`step-nav-${i}`);
    const content = document.getElementById(`step-content-${i}`);
    if (navItem && content) {
      if (i === stepNumber) {
        navItem.classList.add("active");
        content.classList.remove("hidden");
      } else {
        navItem.classList.remove("active");
        content.classList.add("hidden");
      }
    }
  }
}

async function loadLearnerRoles() {
  try {
    const res = await fetch('/api/v1/learner/roles');
    const data = await res.json();
    allLearnerRoles = data.roles || [];
    renderLearnerRolesGrid(allLearnerRoles);
  } catch (err) {
    console.error("Failed to load roles:", err);
  }
}

function filterLearnerRoles(query) {
  const q = query.toLowerCase().trim();
  if (!q) {
    renderLearnerRolesGrid(allLearnerRoles);
    return;
  }

  const filtered = allLearnerRoles.filter(r => {
    const titleMatch = r.title.toLowerCase().includes(q);
    const deptMatch = r.department.toLowerCase().includes(q);
    const descMatch = r.description.toLowerCase().includes(q);
    const compMatch = r.required_competencies.some(c => c.name.toLowerCase().includes(q) || c.code.toLowerCase().includes(q));
    return titleMatch || deptMatch || descMatch || compMatch;
  });

  renderLearnerRolesGrid(filtered);
}

function renderLearnerRolesGrid(roles) {
  const grid = document.getElementById('learner-role-grid');
  grid.innerHTML = '';

  if (roles.length === 0) {
    grid.innerHTML = '<p style="color: var(--text-muted); padding: 1rem;">No matching government roles found for your search query.</p>';
    return;
  }

  roles.forEach(role => {
    const card = document.createElement('div');
    card.className = `glass-card role-card ${selectedRoleId === role.id ? 'selected' : ''}`;
    card.id = `role-card-${role.id}`;
    card.onclick = () => selectRole(role.id);

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <h3 style="color: #172033; font-size: 1.15rem;">${role.title}</h3>
        <span style="font-size: 0.75rem; background: #eff6ff; color: var(--primary); padding: 0.2rem 0.6rem; border-radius: 20px; font-weight: 700;">${role.department}</span>
      </div>
      <p style="font-size: 0.85rem; color: var(--text-muted); margin: 0.6rem 0;">${role.description}</p>
      <p style="font-size: 0.8rem; color: var(--accent-amber); margin-bottom: 0.8rem; font-weight: 600;">
        🎓 <strong>Eligibility Benchmark:</strong> ${role.eligibility}
      </p>
      <div style="margin-top: 0.5rem;">
        <strong style="font-size: 0.8rem; color: var(--text-muted); display: block; margin-bottom: 0.4rem;">Target Competency Benchmarks:</strong>
        ${role.required_competencies.map(c => `
          <span class="competency-tag">${c.name} (${c.target_score}%)</span>
        `).join('')}
      </div>
    `;
    grid.appendChild(card);
  });
}

async function selectRole(roleId) {
  if (!currentUserId) {
    showAuthModal();
    return;
  }
  selectedRoleId = roleId;
  document.querySelectorAll('.role-card').forEach(c => c.classList.remove('selected'));
  const selectedCard = document.getElementById(`role-card-${roleId}`);
  if (selectedCard) selectedCard.classList.add('selected');

  document.getElementById('btn-to-step2').disabled = false;

  try {
    await fetch('/api/v1/learner/select-role', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: currentUserId, role_id: roleId })
    });
  } catch (err) {
    console.error("Error selecting role:", err);
  }
}

async function proceedToBaselineQuiz() {
  if (!selectedRoleId) return;
  switchStep(2);

  try {
    const res = await fetch(`/api/v1/learner/quiz/baseline/${selectedRoleId}`);
    const data = await res.json();
    activeBaselineQuestions = data.questions;
    selectedBaselineAnswers = {};

    const box = document.getElementById('baseline-quiz-box');
    box.innerHTML = `<h3 style="margin-bottom: 1.5rem; color: var(--primary);">Diagnostic Evaluation Questions for ${data.role_title}</h3>`;

    if (activeBaselineQuestions.length === 0) {
      box.innerHTML += '<p style="color: var(--text-muted);">No baseline diagnostic questions created yet for this role.</p>';
      return;
    }

    activeBaselineQuestions.forEach((q, idx) => {
      const qDiv = document.createElement('div');
      qDiv.className = 'question-card';
      qDiv.innerHTML = `
        <p style="font-weight: 700; font-size: 1rem; color: #172033;">
          <span style="color: var(--primary);">Q${idx + 1}.</span> [${q.competency_name}] ${q.question}
        </p>
        <div style="margin-top: 0.8rem;">
          ${q.options.map((opt, optIdx) => `
            <button type="button" class="option-btn" id="q-${q.id}-opt-${optIdx}" onclick="selectBaselineAnswer('${q.id}', ${optIdx})">
              ${String.fromCharCode(65 + optIdx)}. ${opt}
            </button>
          `).join('')}
        </div>
      `;
      box.appendChild(qDiv);
    });
  } catch (err) {
    console.error("Failed to load baseline quiz:", err);
  }
}

function selectBaselineAnswer(qId, optIdx) {
  selectedBaselineAnswers[qId] = optIdx;

  const qObj = activeBaselineQuestions.find(q => q.id === qId);
  if (qObj) {
    qObj.options.forEach((_, idx) => {
      const btn = document.getElementById(`q-${qId}-opt-${idx}`);
      if (btn) {
        if (idx === optIdx) {
          btn.classList.add('selected');
        } else {
          btn.classList.remove('selected');
        }
      }
    });
  }
}

async function submitBaselineQuiz() {
  if (Object.keys(selectedBaselineAnswers).length < activeBaselineQuestions.length) {
    if (!confirm("You have unanswered questions. Submit diagnostic quiz anyway?")) return;
  }

  const payload = {
    user_id: currentUserId,
    role_id: selectedRoleId,
    answers: selectedBaselineAnswers
  };

  try {
    const res = await fetch('/api/v1/learner/quiz/baseline/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (res.ok) {
      renderRadarChart(data.gap_analysis);
      renderGapCards(data.gap_analysis);
      switchStep(3);
    }
  } catch (err) {
    alert("Failed to grade baseline quiz.");
  }
}

function renderRadarChart(gapAnalysis) {
  const labels = gapAnalysis.map(g => g.competency_name);
  const targets = gapAnalysis.map(g => g.target_benchmark);
  const currents = gapAnalysis.map(g => g.current_score);

  const ctx = document.getElementById('gapRadarChart').getContext('2d');
  if (gapRadarChartInstance) {
    gapRadarChartInstance.destroy();
  }

  gapRadarChartInstance = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Required Benchmark (Target %)',
          data: targets,
          borderColor: '#06b6d4',
          backgroundColor: 'rgba(6, 182, 212, 0.15)',
          pointBackgroundColor: '#06b6d4',
          borderWidth: 2
        },
        {
          label: 'Current Employee Score (%)',
          data: currents,
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37, 99, 235, 0.25)',
          pointBackgroundColor: '#2563eb',
          borderWidth: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: '#e2e8f0' },
          grid: { color: '#f1f5f9' },
          pointLabels: { color: '#172033', font: { size: 12, weight: '700' } },
          ticks: { color: '#64748b', backdropColor: 'transparent' },
          min: 0,
          max: 100
        }
      },
      plugins: {
        legend: { labels: { color: '#172033', font: { weight: '600' } } }
      }
    }
  });
}

function renderGapCards(gapAnalysis) {
  const container = document.getElementById('gap-cards-container');
  container.innerHTML = '';

  gapAnalysis.forEach(gap => {
    const card = document.createElement('div');
    card.className = 'glass-card';
    card.style.padding = '1rem 1.25rem';

    const gapColor = gap.gap_score > 30 ? 'var(--accent-red)' : (gap.gap_score > 5 ? 'var(--accent-amber)' : 'var(--accent-green)');

    card.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <strong style="color: #172033; font-size: 1rem;">${gap.competency_name}</strong>
        <span style="color: ${gapColor}; font-weight: 700; font-size: 0.9rem;">
          ${gap.gap_score > 0 ? `Gap: ${gap.gap_score}% Deficit` : '✅ Benchmark Achieved'}
        </span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">
        <span>Current Score: ${gap.current_score}%</span>
        <span>Target Benchmark: ${gap.target_benchmark}%</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width: ${(gap.current_score / gap.target_benchmark) * 100}%;"></div>
      </div>
    `;
    container.appendChild(card);
  });
}

async function fetchAndDisplayRecommendations() {
  switchStep(4);
  const container = document.getElementById('rec-cards-container');
  container.innerHTML = '<p style="color: var(--primary);">⏳ Indexing iGOT Karmayogi Courses & Uploaded Syllabus Materials...</p>';

  const formData = new FormData();
  formData.append('user_id', currentUserId);

  try {
    const res = await fetch('/api/v1/learner/recommendations', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();

    container.innerHTML = '';
    if (data.recommendations.length === 0) {
      container.innerHTML = '<div class="glass-card"><p style="color: var(--accent-green); font-weight: 700;">🎉 Congratulations! All competency benchmark targets have been met. No skill gaps detected.</p></div>';
      return;
    }

    data.recommendations.forEach(rec => {
      const card = document.createElement('div');
      card.className = 'glass-card';
      card.style.display = 'flex';
      card.style.flexDirection = 'column';
      card.style.justifySpaceBetween = 'space-between';

      const isPDF = rec.type === 'CREATOR_DOCUMENT_PDF';

      card.innerHTML = `
        <div>
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
            <span class="urgency-badge urgency-${rec.urgency}">${rec.urgency} DEFICIT</span>
            <span style="font-size: 0.75rem; color: var(--primary); background: #eff6ff; padding: 0.2rem 0.6rem; border-radius: 20px; font-weight: 700;">
              ${isPDF ? '📄 Creator PDF Document' : '🎓 iGOT Course'}
            </span>
          </div>

          <h3 style="color: #172033; font-size: 1.1rem; margin-bottom: 0.4rem;">${rec.title}</h3>
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.6rem;">${rec.provider}</p>
          <p style="font-size: 0.85rem; color: var(--text-light); margin-bottom: 1rem;">${rec.description}</p>
        </div>

        <div>
          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted); border-top: 1px solid var(--border-light); padding-top: 0.75rem; margin-bottom: 1rem;">
            <span>⏱️ ${rec.duration}</span>
            <span>⭐ ${rec.rating} / 5.0</span>
          </div>

          <button class="btn btn-primary" style="width: 100%; justify-content: center;" onclick="handleCourseAction('${rec.id}', '${rec.title.replace(/'/g, "\\'")}', '${rec.type}', '${rec.competency_code}', '${rec.action_url}')">
            ${isPDF ? '📄 Open Syllabus PDF & Take Quiz' : (rec.is_enrolled ? '▶️ Review iGOT Module & Take Quiz' : '🚀 Enroll & Launch iGOT Module')}
          </button>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = '<p style="color: var(--accent-red);">Failed to load recommendations.</p>';
  }
}

async function handleCourseAction(courseId, title, type, compCode, actionUrl) {
  currentActiveCompForIntQuiz = compCode;

  try {
    await fetch('/api/v1/learner/igot/enroll', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: currentUserId, course_id: courseId })
    });
  } catch (err) {
    console.error("Enrollment failed:", err);
  }

  if (type === 'CREATOR_DOCUMENT_PDF') {
    window.open(`/static/docs/${courseId}`, '_blank');
    switchStep(5);
    loadIntermediateQuiz(compCode);
    return;
  }

  launchCoursePlayer(courseId, title, compCode, actionUrl);
}

function launchCoursePlayer(courseId, title, compCode, igotUrl) {
  currentActiveCompForIntQuiz = compCode;

  const modal = document.getElementById('course-modal');
  const modalContent = document.getElementById('modal-content');
  modal.classList.remove('hidden');

  const portalUrl = igotUrl && igotUrl.startsWith('http') ? igotUrl : "https://igotkarmayogi.gov.in/#/";

  modalContent.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
      <div>
        <h2 style="color: #172033;">${title}</h2>
        <p style="color: var(--primary); font-size: 0.9rem; font-weight: 700; margin-top: 0.2rem;">iGOT Karmayogi Official Interactive Training Module</p>
      </div>
      <a href="${portalUrl}" target="_blank" class="btn btn-secondary" style="font-size: 0.85rem; gap: 0.4rem;">
        🔗 Open Course on iGOT Portal ↗
      </a>
    </div>
    
    <div style="background: #f8fafc; border-radius: 12px; border: 1px solid #edf0f4; padding: 1.5rem; margin-bottom: 1.5rem;">
      <h4 style="color: #1e3a8a; margin-bottom: 0.5rem;">📘 Official Module Syllabus & Guidelines</h4>
      <p style="color: #475569; font-size: 0.95rem; line-height: 1.6;">
        This module covers the core competencies required under the National Programme for Civil Services Capacity Building (iGOT Karmayogi Framework). Key topics include operational sampling guidelines, survey data estimation formulas, and data security standards.
      </p>

      <div style="display: flex; gap: 1rem; margin-top: 1.25rem;">
        <div style="flex: 1; background: #ffffff; border-radius: 8px; padding: 0.8rem; border: 1px solid #edf0f4;">
          <span style="font-size: 0.75rem; color: var(--text-muted); display: block;">TARGET COMPETENCY</span>
          <strong style="color: var(--primary);">${compCode}</strong>
        </div>
        <div style="flex: 1; background: #ffffff; border-radius: 8px; padding: 0.8rem; border: 1px solid #edf0f4;">
          <span style="font-size: 0.75rem; color: var(--text-muted); display: block;">GOVERNMENT ISSUER</span>
          <strong style="color: var(--accent-green);">MoSPI / iGOT Karmayogi</strong>
        </div>
      </div>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center;">
      <span style="font-size: 0.85rem; color: var(--accent-green); font-weight: 700;">✅ Status: Course Enrolled & Syllabus Reviewed</span>
      <button class="btn btn-success" onclick="closeCourseModalAndStartQuiz('${compCode}')">
        Take Intermediate Evaluation Quiz & Update Skill Profile ➔
      </button>
    </div>
  `;
}

function closeCourseModal() {
  document.getElementById('course-modal').classList.add('hidden');
}

function closeCourseModalAndStartQuiz(compCode) {
  closeCourseModal();
  switchStep(5);
  loadIntermediateQuiz(compCode);
}

async function loadIntermediateQuiz(compCode) {
  currentActiveCompForIntQuiz = compCode;
  try {
    const res = await fetch(`/api/v1/learner/quiz/intermediate/${compCode}`);
    const data = await res.json();
    activeIntermediateQuestions = data.questions;
    selectedIntermediateAnswers = {};

    const box = document.getElementById('intermediate-quiz-box');
    box.innerHTML = `<p style="color: var(--primary); font-weight: 700; margin-bottom: 1rem;">Testing comprehension for ${compCode}:</p>`;

    activeIntermediateQuestions.forEach((q, idx) => {
      const qDiv = document.createElement('div');
      qDiv.className = 'question-card';
      qDiv.innerHTML = `
        <p style="font-weight: 700; font-size: 0.95rem; color: #172033;">
          Q${idx + 1}. ${q.question}
        </p>
        <div style="margin-top: 0.6rem;">
          ${q.options.map((opt, optIdx) => `
            <button type="button" class="option-btn" id="int-q-${q.id}-opt-${optIdx}" onclick="selectIntermediateAnswer('${q.id}', ${optIdx})">
              ${String.fromCharCode(65 + optIdx)}. ${opt}
            </button>
          `).join('')}
        </div>
      `;
      box.appendChild(qDiv);
    });

    document.getElementById('btn-submit-int-quiz').style.display = 'flex';
  } catch (err) {
    console.error("Failed to load intermediate quiz:", err);
  }
}

function selectIntermediateAnswer(qId, optIdx) {
  selectedIntermediateAnswers[qId] = optIdx;
  const qObj = activeIntermediateQuestions.find(q => q.id === qId);
  if (qObj) {
    qObj.options.forEach((_, idx) => {
      const btn = document.getElementById(`int-q-${qId}-opt-${idx}`);
      if (btn) {
        if (idx === optIdx) {
          btn.classList.add('selected');
        } else {
          btn.classList.remove('selected');
        }
      }
    });
  }
}

async function submitIntermediateQuiz() {
  if (!currentActiveCompForIntQuiz) return;

  const payload = {
    user_id: currentUserId,
    competency_code: currentActiveCompForIntQuiz,
    answers: selectedIntermediateAnswers
  };

  try {
    const res = await fetch('/api/v1/learner/quiz/intermediate/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (res.ok) {
      alert(`🎉 Intermediate Quiz Passed! Score: ${data.quiz_score}%\nCompetency level boosted from ${data.previous_competency_score}% to ${data.updated_competency_score}%!`);
      loadLiveUserProfile();
    }
  } catch (err) {
    alert("Failed to submit intermediate quiz.");
  }
}

async function loadLiveUserProfile() {
  if (!currentUserId) return;
  try {
    const res = await fetch(`/api/v1/learner/profile/${currentUserId}`);
    const data = await res.json();

    const box = document.getElementById('live-profile-box');
    if (!data.role) {
      box.innerHTML = `<p style="color: var(--text-muted);">No active role selected for ${data.name}. Select a role in Step 1.</p>`;
      return;
    }

    let html = `
      <div style="margin-bottom: 1rem;">
        <h4 style="color: var(--primary); font-size: 1.1rem;">${data.name}</h4>
        <p style="font-size: 0.85rem; color: var(--text-muted);">${data.role.title} (${data.role.department})</p>
      </div>

      <h5 style="color: #172033; margin-bottom: 0.5rem; font-weight: 700;">Competency Status:</h5>
      <div style="display: flex; flex-direction: column; gap: 0.8rem;">
    `;

    data.competencies.forEach(c => {
      const isOk = c.gap <= 5.0;
      html += `
        <div style="background: #f8fafc; border: 1px solid ${isOk ? '#a7f3d0' : '#edf0f4'}; padding: 0.75rem; border-radius: 10px;">
          <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
            <strong style="color: #172033;">${c.name}</strong>
            <span style="color: ${isOk ? 'var(--accent-green)' : 'var(--accent-amber)'}; font-weight: 700;">
              ${c.current_score}% / ${c.target_benchmark}% ${isOk ? '✅' : '(Gap: ' + c.gap + '%)'}
            </span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width: ${Math.min(100, (c.current_score / c.target_benchmark) * 100)}%; background: ${isOk ? 'var(--accent-green)' : 'var(--primary)'};"></div>
          </div>
        </div>
      `;
    });

    html += `</div><h5 style="color: #172033; margin-top: 1.5rem; margin-bottom: 0.5rem; font-weight: 700;">Earned iGOT Badges:</h5>`;

    if (data.badges.length === 0) {
      html += '<p style="font-size: 0.85rem; color: var(--text-muted);">No badges earned yet. Complete intermediate evaluation quizzes to earn badges.</p>';
    } else {
      data.badges.forEach(b => {
        html += `
          <div class="badge-card">
            <div class="badge-icon">🏅</div>
            <div>
              <strong style="color: #172033; font-size: 0.9rem;">${b.title}</strong>
              <p style="font-size: 0.75rem; color: var(--text-muted);">Issued: ${new Date(b.issued_at).toLocaleDateString()}</p>
            </div>
          </div>
        `;
      });
    }

    box.innerHTML = html;
  } catch (err) {
    console.error("Profile load failed:", err);
  }
}
