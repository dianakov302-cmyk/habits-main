import { apiRequest, USER_EMAIL_KEY, isAuthenticated, removeToken } from './api.js';

// ── State ──
let email = null;
let srQueue = [];
let srCurrentCard = null;
let selectedDeloadActivity = null;
let activeBrainstormId = null;
let brainstormSessions = [];
let currentConvId = null;
let rewardCatalogData = [];
let userUnlocked = [];

// ── Auth verification ──
async function verifyAuth() {
  if (!isAuthenticated()) {
    showAuthGate();
    return null;
  }
  try {
    const result = await apiRequest('/users/me');
    if (result && result.authenticated) {
      return result.email;
    }
  } catch (e) {}
  showAuthGate();
  return null;
}

// ── Bootstrap ──
document.addEventListener('DOMContentLoaded', async () => {
  initTabs();

  const verifiedEmail = await verifyAuth();
  if (!verifiedEmail) return;

  email = verifiedEmail;
  // Also keep localStorage in sync for display purposes
  localStorage.setItem(USER_EMAIL_KEY, email);

  updateNavUser();
  await loadOverview();
  loadRewardCatalog();
});

// ── Auth gate ──
function showAuthGate() {
  const gate = document.getElementById('overviewAuth');
  const content = document.getElementById('overviewContent');
  if (gate) gate.style.display = 'block';
  if (content) content.style.display = 'none';
}

function updateNavUser() {
  const el = document.getElementById('dashEmail');
  const av = document.getElementById('dashAvatar');
  if (!el || !av) return;
  if (email) {
    el.textContent = email;
    av.textContent = email[0].toUpperCase();
    av.onclick = () => {
      if (confirm(`Sign out of ${email}?`)) {
        removeToken();
        localStorage.removeItem(USER_EMAIL_KEY);
        window.location.href = 'registration.html';
      }
    };
  } else {
    el.textContent = '';
    av.textContent = '?';
    av.onclick = () => { window.location.href = 'registration.html'; };
  }
}

// ── Tab navigation ──
function initTabs() {
  const tabs = document.querySelectorAll('.dash-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => switchPanel(tab.dataset.panel));
  });
}

window.switchPanel = function switchPanel(name) {
  document.querySelectorAll('.dash-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.dash-tab').forEach(t => t.classList.remove('active'));
  const panel = document.getElementById(`panel-${name}`);
  const tab = document.querySelector(`.dash-tab[data-panel="${name}"]`);
  if (panel) panel.classList.add('active');
  if (tab) tab.classList.add('active');
  onPanelActivate(name);
};

async function onPanelActivate(name) {
  if (!email) return;
  if (name === 'protocol') await loadProtocol();
  if (name === 'program')  await loadProgram();
  if (name === 'review')   await loadReview();
  if (name === 'productivity') { await loadWater(); await loadPlanner(); }
  if (name === 'study')    { await loadSRQueue(); await loadBrainstorm(); }
  if (name === 'rewards')  await loadUserRewards();
  if (name === 'chat')     await loadConversations();
}

// ── Helper ──
function today() { return new Date().toISOString().slice(0, 10); }
function status(id, msg, type = 'ok') {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = msg;
  el.className = `status-msg ${type}`;
}
function greeting() {
  const h = new Date().getHours();
  if (h < 12) return 'Good morning.';
  if (h < 18) return 'Good afternoon.';
  return 'Good evening.';
}

// ════════════════════════════════════════════════
//  OVERVIEW
// ════════════════════════════════════════════════
async function loadOverview() {
  const greet = document.getElementById('greetingText');
  if (greet) greet.textContent = greeting();

  await Promise.allSettled([
    loadIdentity(),
    loadProtocolSummary(),
    loadDeloadAlert(),
  ]);
}

async function loadIdentity() {
  try {
    const res = await apiRequest(`/identity/profile?email=${encodeURIComponent(email)}`);
    const d = res.data || {};
    set('identityLevel', d.level || 'Lost');
    set('identityMsg', d.message || '');
    const score = d.score ?? 0;
    const bar = document.getElementById('identityBar');
    if (bar) bar.style.width = `${Math.min(100, score)}%`;
    set('identityNext', d.next_level
      ? `Next: ${d.next_level} — ${100 - score > 0 ? Math.round(100 - score) : 0} pts away`
      : 'Maximum level reached');
    set('statStreak', d.current_streak ?? '—');
    set('statPoints', d.today_points ?? '—');
  } catch (_) {
    set('identityLevel', 'Lost');
    set('identityMsg', 'Start tracking habits to build your identity score.');
    set('identityNext', '');
  }
}

async function loadProtocolSummary() {
  try {
    const res = await apiRequest(`/protocol/today?email=${encodeURIComponent(email)}`);
    const c = document.getElementById('protocolSummaryContent');
    if (!c) return;
    if (!res.data) { c.innerHTML = '<div class="empty">No protocol set for today. Go to Protocol tab to create one.</div>'; return; }
    const d = res.data;
    c.innerHTML = buildTaskRowHtml('minimum', d.minimum_task, false) +
      buildTaskRowHtml('target', d.target_task, false) +
      buildTaskRowHtml('bonus', d.bonus_task, false);
    set('statPoints', d.points_earned ?? '—');
  } catch (_) {}
}

async function loadDeloadAlert() {
  try {
    const res = await apiRequest(`/deload/status?email=${encodeURIComponent(email)}`);
    const alert = document.getElementById('deloadAlert');
    if (alert && res.data?.active && !res.data?.deload?.completed) {
      alert.style.display = 'block';
    }
  } catch (_) {}
}

async function loadWaterStat() {
  try {
    const res = await apiRequest(`/productivity/water?email=${encodeURIComponent(email)}&date=${today()}`);
    set('statWater', res.data?.count ?? 0);
  } catch (_) { set('statWater', '—'); }
}

async function loadCardsStat() {
  try {
    const res = await apiRequest(`/productivity/sr/review?email=${encodeURIComponent(email)}`);
    set('statCards', (res.data || []).length);
  } catch (_) { set('statCards', '—'); }
}

// ════════════════════════════════════════════════
//  DAILY PROTOCOL
// ════════════════════════════════════════════════
async function loadProtocol() {
  try {
    const res = await apiRequest(`/protocol/today?email=${encodeURIComponent(email)}`);
    if (!res.data) {
      showEl('protocolCreateForm'); hideEl('protocolActive');
    } else {
      hideEl('protocolCreateForm'); showEl('protocolActive');
      renderProtocolTasks(res.data);
    }
  } catch (_) {
    showEl('protocolCreateForm'); hideEl('protocolActive');
  }
  await loadDeloadPanel();
}

function buildTaskRowHtml(type, task, interactive = true) {
  if (!task) return '';
  const badges = { minimum: 'badge-min', target: 'badge-tgt', bonus: 'badge-bon' };
  const pts = { minimum: 1, target: 2, bonus: 3 };
  const labels = { minimum: 'MIN', target: 'TGT', bonus: 'BON' };
  const done = task.completed;
  const btn = interactive && !done
    ? `<button class="check-btn" onclick="completeTask('${type}')">Done</button>`
    : (done ? '<span style="color:#10b981;font-size:.8rem">✓</span>' : '');
  return `<div class="task-row ${done ? 'completed' : ''}">
    <span class="task-badge ${badges[type]}">${labels[type]}</span>
    <span class="task-name">${escHtml(task.title)}</span>
    <span class="task-pts">${pts[type]} pt${pts[type] > 1 ? 's' : ''}</span>
    ${btn}
  </div>`;
}

function renderProtocolTasks(d) {
  const list = document.getElementById('protocolTaskList');
  if (list) {
    list.innerHTML = buildTaskRowHtml('minimum', d.minimum_task) +
      buildTaskRowHtml('target', d.target_task) +
      buildTaskRowHtml('bonus', d.bonus_task);
  }
  const pts = document.getElementById('protocolPoints');
  if (pts) pts.textContent = `${d.points_earned ?? 0} pts`;
}

document.getElementById('protocolCreateBtn')?.addEventListener('click', async () => {
  const min = val('pMinInput'), tgt = val('pTargetInput'), bon = val('pBonusInput');
  if (!min || !tgt || !bon) { status('protocolCreateStatus', 'All three tasks are required.', 'err'); return; }
  try {
    const res = await apiRequest('/protocol/create', {
      method: 'POST',
      body: JSON.stringify({ email, date: today(), minimum_task: min, target_task: tgt, bonus_task: bon }),
    });
    if (res.status === 'success') {
      hideEl('protocolCreateForm'); showEl('protocolActive');
      renderProtocolTasks(res.data);
      status('protocolCreateStatus', '', 'ok');
    } else {
      status('protocolCreateStatus', res.message || 'Failed.', 'err');
    }
  } catch (e) { status('protocolCreateStatus', e.message, 'err'); }
});

window.completeTask = async function(taskType) {
  try {
    const res = await apiRequest('/protocol/complete-task', {
      method: 'POST',
      body: JSON.stringify({ email, date: today(), task_type: taskType }),
    });
    if (res.status === 'success') {
      renderProtocolTasks(res.data);
      status('protocolStatus', res.data.streak_counts ? '✓ Streak maintained' : '✓ Task done', 'ok');
    } else {
      status('protocolStatus', res.message || 'Error', 'err');
    }
  } catch (e) { status('protocolStatus', e.message, 'err'); }
};

// ── Deload panel ──
const DELOAD_ACTIVITIES = [
  { id: 'walking',       icon: '🚶', label: 'Walking' },
  { id: 'stretching',    icon: '🧘', label: 'Stretching' },
  { id: 'meditation',    icon: '🧠', label: 'Meditation' },
  { id: 'journaling',    icon: '📝', label: 'Journaling' },
  { id: 'light_reading', icon: '📖', label: 'Light Reading' },
];

async function loadDeloadPanel() {
  try {
    const res = await apiRequest(`/deload/status?email=${encodeURIComponent(email)}`);
    const d = res.data || {};
    const panel = document.getElementById('deloadPanel');
    if (!panel) return;
    if (d.active && !d.deload?.completed) {
      showEl('deloadPanel');
      const grid = document.getElementById('activityGrid');
      if (grid) {
        grid.innerHTML = DELOAD_ACTIVITIES.map(a =>
          `<button class="activity-btn" data-id="${a.id}" onclick="selectActivity('${a.id}')">
            <div class="activity-icon">${a.icon}</div>
            <div class="activity-label">${a.label}</div>
          </button>`
        ).join('');
      }
    } else {
      hideEl('deloadPanel');
    }
  } catch (_) { hideEl('deloadPanel'); }
}

window.selectActivity = function(id) {
  selectedDeloadActivity = id;
  document.querySelectorAll('.activity-btn').forEach(b => {
    b.classList.toggle('selected', b.dataset.id === id);
  });
  const btn = document.getElementById('deloadCompleteBtn');
  if (btn) btn.disabled = false;
};

document.getElementById('deloadCompleteBtn')?.addEventListener('click', async () => {
  if (!selectedDeloadActivity) return;
  try {
    const res = await apiRequest('/deload/complete', {
      method: 'POST',
      body: JSON.stringify({ email, activity: selectedDeloadActivity }),
    });
    if (res.status === 'success') {
      status('deloadStatus', '✓ Recovery day complete! Streak maintained.', 'ok');
      setTimeout(() => { hideEl('deloadPanel'); hideEl('deloadAlert'); }, 1500);
    } else {
      status('deloadStatus', res.message || 'Error', 'err');
    }
  } catch (e) { status('deloadStatus', e.message, 'err'); }
});

// ════════════════════════════════════════════════
//  30-DAY PROGRAM
// ════════════════════════════════════════════════
async function loadProgram() {
  try {
    const res = await apiRequest(`/program/status?email=${encodeURIComponent(email)}`);
    if (res.data !== null && res.data !== undefined) {
      showEl('programActive'); hideEl('programStart');
      renderProgramStatus(res.data);
    } else {
      hideEl('programActive'); showEl('programStart');
      await loadPhases();
    }
  } catch (_) { hideEl('programActive'); showEl('programStart'); await loadPhases(); }
}

async function loadPhases() {
  try {
    const res = await apiRequest('/program/phases');
    const c = document.getElementById('programPhasesContent');
    if (!c) return;
    if (!res.data?.length) { c.innerHTML = '<div class="empty">No phase data.</div>'; return; }
    c.innerHTML = res.data.map(p =>
      `<div style="margin-bottom:14px">
        <span class="phase-chip phase-${p.phase}">${p.phase}</span>
        <span style="font-size:.78rem;color:var(--muted);margin-left:10px">Days ${p.days}</span>
        <div style="font-size:.85rem;color:var(--muted);margin-top:4px">${escHtml(p.description || '')}</div>
      </div>`
    ).join('');
  } catch (_) {}
}

function renderProgramStatus(d) {
  const day = d.current_day ?? 1;
  const total = 30;
  const remain = Math.max(0, total - day + 1);
  set('programDay', day);
  set('programRemain', remain);
  const bar = document.getElementById('programProgressBar');
  if (bar) bar.style.width = `${Math.round((day / total) * 100)}%`;
  const chip = document.getElementById('programPhaseChip');
  const phase = d.current_phase || d.phase || '';
  if (chip) { chip.textContent = phase; chip.className = `phase-chip phase-${phase}`; }
  const tasks = document.getElementById('programTasks');
  if (tasks) {
    const list = d.today_tasks || [];
    tasks.innerHTML = list.length
      ? list.map(t => `<div class="task-row"><span class="task-name">${escHtml(t)}</span></div>`).join('')
      : '<div class="empty">Rest day or tasks not set.</div>';
  }
  buildDayGrid(day);
}

function buildDayGrid(current) {
  const grid = document.getElementById('programDayGrid');
  if (!grid) return;
  grid.innerHTML = Array.from({ length: 30 }, (_, i) => {
    const n = i + 1;
    const cls = n < current ? 'done' : n === current ? 'current' : '';
    return `<div class="day-dot ${cls}">${n}</div>`;
  }).join('');
}

document.getElementById('programStartBtn')?.addEventListener('click', async () => {
  const goal = val('programGoalSelect');
  const level = val('programLevelSelect');
  if (!goal) { status('programStartStatus', 'Select a goal.', 'err'); return; }
  try {
    const res = await apiRequest('/program/start', {
      method: 'POST',
      body: JSON.stringify({ email, goal_code: goal, level }),
    });
    if (res.status === 'success') {
      showEl('programActive'); hideEl('programStart');
      await loadProgram();
    } else { status('programStartStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('programStartStatus', e.message, 'err'); }
});

document.getElementById('programCompleteDayBtn')?.addEventListener('click', async () => {
  try {
    const res = await apiRequest('/program/complete-day', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
    if (res.status === 'success') {
      status('programDayStatus', '✓ Day complete!', 'ok');
      await loadProgram();
    } else { status('programDayStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('programDayStatus', e.message, 'err'); }
});

// ════════════════════════════════════════════════
//  WEEKLY REVIEW
// ════════════════════════════════════════════════
async function loadReview() {
  await loadReviewHistory();
}

async function loadReviewHistory() {
  try {
    const res = await apiRequest(`/reviews/history?email=${encodeURIComponent(email)}`);
    const list = document.getElementById('reviewHistoryList');
    if (!list) return;
    const items = res.data || [];
    if (!items.length) { list.innerHTML = '<div class="empty">No reviews yet.</div>'; return; }
    list.innerHTML = items.slice(0, 5).map(r =>
      `<div style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,.06)">
        <div style="font-size:.75rem;color:var(--muted);margin-bottom:4px">${r.date || ''}</div>
        <div style="font-size:.82rem">${escHtml(r.what_worked || '')}</div>
      </div>`
    ).join('');
  } catch (_) {}
}

document.getElementById('reviewSubmitBtn')?.addEventListener('click', async () => {
  const worked = val('reviewWorked'), dist = val('reviewDistracted'), change = val('reviewChange');
  if (!worked || !dist || !change) { status('reviewStatus', 'Fill in all three questions.', 'err'); return; }
  try {
    const res = await apiRequest('/reviews/submit', {
      method: 'POST',
      body: JSON.stringify({ email, what_worked: worked, what_distracted: dist, what_to_change: change }),
    });
    if (res.status === 'success') {
      status('reviewStatus', '✓ Review saved.', 'ok');
      const card = document.getElementById('reviewResultCard');
      if (card) {
        showEl('reviewResultCard');
        set('reviewReflectionText', res.data?.reflection || '');
        const ul = document.getElementById('reviewSuggestionsList');
        if (ul) ul.innerHTML = (res.data?.suggestions || []).map(s => `<li>${escHtml(s)}</li>`).join('');
      }
      await loadReviewHistory();
    } else { status('reviewStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('reviewStatus', e.message, 'err'); }
});

// ════════════════════════════════════════════════
//  WATER TRACKER
// ════════════════════════════════════════════════
async function loadWater() {
  try {
    const res = await apiRequest(`/productivity/water?email=${encodeURIComponent(email)}&date=${today()}`);
    renderWater(res.data || { count: 0, goal_glasses: 8 });
  } catch (_) { renderWater({ count: 0, goal_glasses: 8 }); }
}

function renderWater(d) {
  const count = d.glasses ?? d.count ?? 0;
  const goal = d.goal ?? d.goal_glasses ?? 8;
  set('waterCount', count);
  const goalEl = document.getElementById('waterGoal');
  if (goalEl) goalEl.textContent = goal;
  const glasses = document.getElementById('waterGlasses');
  if (glasses) {
    glasses.innerHTML = Array.from({ length: goal }, (_, i) =>
      `<div class="glass ${i < count ? 'filled' : ''}">💧</div>`
    ).join('');
  }
  const bar = document.getElementById('waterBar');
  if (bar) bar.style.width = `${Math.min(100, Math.round((count / goal) * 100))}%`;
  set('statWater', count);
}

document.getElementById('logWaterBtn')?.addEventListener('click', async () => {
  try {
    const res = await apiRequest('/productivity/water/log', {
      method: 'POST',
      body: JSON.stringify({ email, date: today(), amount_ml: 250 }),
    });
    if (res.status === 'success') {
      renderWater(res.data);
      status('waterStatus', '✓ Glass logged.', 'ok');
    } else { status('waterStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('waterStatus', e.message, 'err'); }
});

// ════════════════════════════════════════════════
//  PLANNER
// ════════════════════════════════════════════════
async function loadPlanner() {
  try {
    const res = await apiRequest(`/productivity/planner?email=${encodeURIComponent(email)}&date=${today()}`);
    renderPlanner(res.data || []);
  } catch (_) { renderPlanner([]); }
}

function renderPlanner(tasks) {
  const list = document.getElementById('plannerList');
  if (!list) return;
  if (!tasks.length) { list.innerHTML = '<div class="empty">No tasks yet.</div>'; return; }
  list.innerHTML = tasks.map(t => {
    const pid = t._id || t.id || '';
    return `<div class="planner-task ${t.completed ? 'done' : ''}" id="ptask-${pid}">
      <div class="priority-dot p-${t.priority || 'medium'}"></div>
      <span class="task-name">${escHtml(t.title)}</span>
      <span style="font-size:.75rem;color:var(--muted);margin-left:auto">${escHtml(t.time_slot || '')}</span>
      ${!t.completed ? `<button class="check-btn" style="margin-left:8px" onclick="completeTask2('${pid}')">Done</button>` : ''}
      <button class="check-btn" style="margin-left:4px;border-color:rgba(239,68,68,.3)" onclick="deleteTask('${pid}')">✕</button>
    </div>`;
  }).join('');
}

window.completeTask2 = async function(id) {
  try {
    await apiRequest(`/productivity/planner/${id}/complete`, {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
    await loadPlanner();
  } catch (e) { status('plannerStatus', e.message, 'err'); }
};

window.deleteTask = async function(id) {
  try {
    await apiRequest(`/productivity/planner/${id}?email=${encodeURIComponent(email)}`, { method: 'DELETE' });
    await loadPlanner();
  } catch (e) { status('plannerStatus', e.message, 'err'); }
};

document.getElementById('plannerAddBtn')?.addEventListener('click', async () => {
  const title = val('plannerTitle');
  if (!title) { status('plannerStatus', 'Enter a task title.', 'err'); return; }
  try {
    const res = await apiRequest('/productivity/planner', {
      method: 'POST',
      body: JSON.stringify({
        email, date: today(),
        title, priority: val('plannerPriority') || 'medium',
        time_slot: val('plannerSlot') || '',
      }),
    });
    if (res.status === 'success') {
      document.getElementById('plannerTitle').value = '';
      document.getElementById('plannerSlot').value = '';
      status('plannerStatus', '✓ Task added.', 'ok');
      await loadPlanner();
    } else { status('plannerStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('plannerStatus', e.message, 'err'); }
});

// ════════════════════════════════════════════════
//  SPACED REPETITION
// ════════════════════════════════════════════════
async function loadSRQueue() {
  try {
    const res = await apiRequest(`/productivity/sr/review?email=${encodeURIComponent(email)}`);
    srQueue = res.data || [];
    set('srDueCount', srQueue.length ? `${srQueue.length} due` : '');
    set('statCards', srQueue.length);
    showNextSRCard();
  } catch (_) { srQueue = []; showNextSRCard(); }
}

function showNextSRCard() {
  const empty = document.getElementById('srEmptyState');
  const done = document.getElementById('srDoneState');
  const review = document.getElementById('srReviewMode');

  if (!srQueue.length) {
    hideEl('srReviewMode');
    if (empty) empty.style.display = 'block';
    if (done) done.style.display = 'none';
    return;
  }

  srCurrentCard = srQueue[0];
  if (empty) empty.style.display = 'none';
  if (done) done.style.display = 'none';
  showEl('srReviewMode');

  set('srCardFace', srCurrentCard.front);
  const answerWrap = document.getElementById('srAnswerWrap');
  if (answerWrap) answerWrap.style.display = 'none';
  const backEl = document.getElementById('srCardBack');
  if (backEl) backEl.textContent = srCurrentCard.back || '';
  status('srStatus', '', 'ok');
}

document.getElementById('srCardFace')?.addEventListener('click', () => {
  const wrap = document.getElementById('srAnswerWrap');
  if (wrap) wrap.style.display = 'block';
});

document.querySelectorAll('.ease-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    if (!srCurrentCard) return;
    const ease = parseInt(btn.dataset.ease, 10);
    try {
      await apiRequest(`/productivity/sr/cards/${srCurrentCard._id || srCurrentCard.id}/review`, {
        method: 'POST',
        body: JSON.stringify({ ease }),
      });
      srQueue.shift();
      set('srDueCount', srQueue.length ? `${srQueue.length} due` : '');
      set('statCards', srQueue.length);
      if (srQueue.length === 0) {
        hideEl('srReviewMode');
        const done = document.getElementById('srDoneState');
        if (done) done.style.display = 'block';
      } else {
        showNextSRCard();
      }
    } catch (e) { status('srStatus', e.message, 'err'); }
  });
});

document.getElementById('srAddBtn')?.addEventListener('click', async () => {
  const deck = val('srDeck'), front = val('srFront'), back = val('srBack');
  if (!front || !back) { status('srAddStatus', 'Front and back are required.', 'err'); return; }
  try {
    const res = await apiRequest('/productivity/sr/cards', {
      method: 'POST',
      body: JSON.stringify({ email, deck: deck || 'Default', front, back }),
    });
    if (res.status === 'success') {
      document.getElementById('srFront').value = '';
      document.getElementById('srBack').value = '';
      status('srAddStatus', '✓ Card added.', 'ok');
      await loadSRQueue();
    } else { status('srAddStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('srAddStatus', e.message, 'err'); }
});

// ════════════════════════════════════════════════
//  BRAINSTORM
// ════════════════════════════════════════════════
async function loadBrainstorm() {
  try {
    const res = await apiRequest(`/productivity/brainstorm?email=${encodeURIComponent(email)}`);
    brainstormSessions = res.data || [];
    renderBrainstormList(brainstormSessions);
  } catch (_) { brainstormSessions = []; renderBrainstormList([]); }
}

function renderBrainstormList(sessions) {
  const list = document.getElementById('brainstormList');
  if (!list) return;
  hideEl('brainstormActive');
  if (!sessions.length) { list.innerHTML = '<div class="empty">No sessions yet.</div>'; return; }
  list.innerHTML = sessions.map(s => {
    const sid = s._id || s.id || '';
    const count = (s.ideas || []).length;
    return `<div class="conv-item" onclick="openBrainstorm('${sid}')">
      <div class="conv-avatar">💡</div>
      <div class="conv-info">
        <div class="conv-name">${escHtml(s.title)}</div>
        <div class="conv-last">${count} idea${count !== 1 ? 's' : ''}</div>
      </div>
    </div>`;
  }).join('');
}

window.openBrainstorm = function(id) {
  activeBrainstormId = id;
  const session = brainstormSessions.find(s => (s._id || s.id) === id);
  hideEl('brainstormList');
  showEl('brainstormActive');
  set('brainstormTitle', session?.title || '');
  renderBrainstormIdeas(session?.ideas || []);
};

function renderBrainstormIdeas(ideas) {
  const c = document.getElementById('brainstormIdeas');
  if (!c) return;
  c.innerHTML = ideas.length
    ? ideas.map(i => `<div class="brainstorm-idea">${escHtml(i.content || i)}<div class="brainstorm-time">${i.added_at || ''}</div></div>`).join('')
    : '<div class="empty">No ideas yet. Add one below.</div>';
}

document.getElementById('brainstormBackBtn')?.addEventListener('click', async () => {
  activeBrainstormId = null;
  hideEl('brainstormActive');
  await loadBrainstorm();
});

document.getElementById('brainstormAddIdeaBtn')?.addEventListener('click', async () => {
  if (!activeBrainstormId) return;
  const content = val('brainstormIdeaInput');
  if (!content) return;
  try {
    const res = await apiRequest(`/productivity/brainstorm/${activeBrainstormId}/ideas`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    });
    if (res.status === 'success') {
      document.getElementById('brainstormIdeaInput').value = '';
      status('brainstormIdeaStatus', '✓ Idea added.', 'ok');
      // Re-fetch sessions and refresh view with updated ideas
      const fetch = await apiRequest(`/productivity/brainstorm?email=${encodeURIComponent(email)}`);
      brainstormSessions = fetch.data || [];
      const session = brainstormSessions.find(s => (s._id || s.id) === activeBrainstormId);
      renderBrainstormIdeas(session?.ideas || []);
    } else { status('brainstormIdeaStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('brainstormIdeaStatus', e.message, 'err'); }
});

document.getElementById('brainstormCreateBtn')?.addEventListener('click', async () => {
  const title = val('brainstormNewTitle');
  if (!title) { status('brainstormStatus', 'Enter a session title.', 'err'); return; }
  try {
    const res = await apiRequest('/productivity/brainstorm', {
      method: 'POST',
      body: JSON.stringify({ email, title }),
    });
    if (res.status === 'success') {
      document.getElementById('brainstormNewTitle').value = '';
      status('brainstormStatus', '✓ Session created.', 'ok');
      await loadBrainstorm();
    } else { status('brainstormStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('brainstormStatus', e.message, 'err'); }
});

// ════════════════════════════════════════════════
//  REWARDS
// ════════════════════════════════════════════════
async function loadRewardCatalog() {
  try {
    const res = await apiRequest('/rewards/catalog');
    rewardCatalogData = res.data || [];
    renderRewardCatalog();
  } catch (_) {}
}

async function loadUserRewards() {
  try {
    const res = await apiRequest(`/rewards/user?email=${encodeURIComponent(email)}`);
    userUnlocked = res.data?.unlocked_rewards || [];
    renderRewardCatalog();
  } catch (_) {}
}

function renderRewardCatalog() {
  const grid = document.getElementById('rewardCatalog');
  if (!grid || !rewardCatalogData.length) return;
  grid.innerHTML = rewardCatalogData.map(r => {
    const unlocked = userUnlocked.includes(r.id);
    return `<div class="reward-card ${unlocked ? 'unlocked' : ''}">
      <div class="reward-icon">${r.icon || '🎁'}</div>
      <div class="reward-name">${escHtml(r.name)}</div>
      <div class="reward-desc">${escHtml(r.description || '')}</div>
      ${unlocked
        ? `<button class="reward-activate-btn" onclick="activateReward('${r.id}')">Activate</button>`
        : `<div class="reward-locked">🔒 ${r.unlock_condition || ''}</div>`}
    </div>`;
  }).join('');
}

document.getElementById('rewardCheckBtn')?.addEventListener('click', async () => {
  const streak = parseInt(val('rewardStreakInput') || '0', 10);
  const programs = parseInt(val('rewardProgramInput') || '0', 10);
  const reviews = parseInt(val('rewardReviewInput') || '0', 10);
  try {
    const res = await apiRequest('/rewards/check-unlock', {
      method: 'POST',
      body: JSON.stringify({ email, current_streak: streak, completed_programs: programs, weekly_reviews: reviews }),
    });
    if (res.status === 'success') {
      const newly = res.data?.newly_unlocked || [];
      status('rewardCheckStatus',
        newly.length ? `✓ Unlocked: ${newly.join(', ')}` : '✓ No new unlocks. Keep going!', 'ok');
      await loadUserRewards();
    } else { status('rewardCheckStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('rewardCheckStatus', e.message, 'err'); }
});

window.activateReward = async function(id) {
  try {
    const res = await apiRequest('/rewards/activate', {
      method: 'POST',
      body: JSON.stringify({ email, reward_code: id }),
    });
    if (res.status === 'success') {
      status('rewardCheckStatus', '✓ Reward activated.', 'ok');
    }
  } catch (_) {}
};

// ════════════════════════════════════════════════
//  CHAT
// ════════════════════════════════════════════════
async function loadConversations() {
  try {
    const res = await apiRequest(`/chat/conversations?email=${encodeURIComponent(email)}`);
    renderConvList(res.data || []);
  } catch (_) { renderConvList([]); }
}

function renderConvList(convs) {
  const list = document.getElementById('convList');
  if (!list) return;
  if (!convs.length) { list.innerHTML = '<div class="empty">No conversations yet.</div>'; return; }
  list.innerHTML = convs.map(c => {
    const cid = c._id || c.id || '';
    const other = c.participants?.find(p => p !== email) || c.title || 'User';
    return `<div class="conv-item" onclick="openConversation('${cid}','${escAttr(other)}')">
      <div class="conv-avatar">${(other[0] || '?').toUpperCase()}</div>
      <div class="conv-info">
        <div class="conv-name">${escHtml(other)}</div>
        <div class="conv-last">${escHtml(c.last_message || 'No messages yet')}</div>
      </div>
    </div>`;
  }).join('');
}

window.openConversation = async function(id, title) {
  currentConvId = id;
  set('chatThreadTitle', title);
  showEl('chatThreadCard');
  hideEl('chatPlaceholderCard');
  await loadMessages(id);
};

async function loadMessages(id) {
  try {
    const res = await apiRequest(`/chat/conversations/${id}/messages?email=${encodeURIComponent(email)}`);
    renderMessages(res.data || []);
  } catch (_) { renderMessages([]); }
}

function renderMessages(msgs) {
  const list = document.getElementById('msgList');
  if (!list) return;
  if (!msgs.length) { list.innerHTML = '<div class="empty" style="text-align:center;padding:20px">No messages yet.</div>'; return; }
  list.innerHTML = msgs.map(m => {
    const mine = m.sender_email === email;
    return `<div class="msg ${mine ? 'mine' : 'theirs'}">
      <div class="msg-bubble">${escHtml(m.content)}</div>
      <div class="msg-time">${m.created_at ? new Date(m.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''}</div>
    </div>`;
  }).join('');
  list.scrollTop = list.scrollHeight;
}

document.getElementById('chatBackBtn')?.addEventListener('click', () => {
  currentConvId = null;
  hideEl('chatThreadCard');
  showEl('chatPlaceholderCard');
});

document.getElementById('msgSendBtn')?.addEventListener('click', sendMessage);
document.getElementById('msgInput')?.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } });

async function sendMessage() {
  if (!currentConvId) return;
  const content = val('msgInput');
  if (!content) return;
  try {
    const res = await apiRequest(`/chat/conversations/${currentConvId}/messages`, {
      method: 'POST',
      body: JSON.stringify({ sender_email: email, content }),
    });
    if (res.status === 'success') {
      document.getElementById('msgInput').value = '';
      await loadMessages(currentConvId);
      status('chatStatus', '', 'ok');
    } else { status('chatStatus', res.message || 'Error', 'err'); }
  } catch (e) { status('chatStatus', e.message, 'err'); }
}

document.getElementById('chatSearchBtn')?.addEventListener('click', async () => {
  const query = val('chatSearchInput');
  if (!query) return;
  try {
    const res = await apiRequest(`/chat/search-users?email=${encodeURIComponent(email)}&query=${encodeURIComponent(query)}`);
    const results = res.data || [];
    const c = document.getElementById('chatSearchResults');
    if (!c) return;
    c.style.display = 'block';
    if (!results.length) { c.innerHTML = '<div style="font-size:.82rem;color:var(--muted)">No users found.</div>'; return; }
    c.innerHTML = results.map(u =>
      `<div class="conv-item" style="margin-bottom:6px" onclick="startDM('${escAttr(u.email || u)}')">
        <div class="conv-avatar">${(u.email || u)[0].toUpperCase()}</div>
        <div class="conv-info"><div class="conv-name">${escHtml(u.email || u)}</div></div>
      </div>`
    ).join('');
  } catch (e) { status('chatStatus', e.message, 'err'); }
});

window.startDM = async function(recipient) {
  try {
    const res = await apiRequest('/chat/conversations', {
      method: 'POST',
      body: JSON.stringify({ sender_email: email, recipient_email: recipient }),
    });
    if (res.status === 'success') {
      const id = res.data?.conversation_id || res.data?._id;
      if (id) window.openConversation(id, recipient);
      await loadConversations();
    }
  } catch (e) { status('chatStatus', e.message, 'err'); }
};

// ════════════════════════════════════════════════
//  Tiny DOM helpers
// ════════════════════════════════════════════════
function val(id) {
  const el = document.getElementById(id);
  return el ? el.value.trim() : '';
}

function set(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function showEl(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = '';
}

function hideEl(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

function escHtml(str) {
  return String(str ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function escAttr(str) {
  return String(str ?? '').replace(/'/g, "\\'").replace(/"/g, '&quot;');
}
