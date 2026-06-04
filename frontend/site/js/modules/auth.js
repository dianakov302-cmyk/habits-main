import { apiRequest, USER_EMAIL_KEY, getToken, setToken, removeToken, isAuthenticated } from './api.js';

/* ── State ── */
let _currentUser = null; // { email }

/* ── Public helpers ── */

export function getCurrentUser() {
  if (_currentUser) return _currentUser;
  const email = localStorage.getItem(USER_EMAIL_KEY);
  if (email && isAuthenticated()) {
    _currentUser = { email };
    return _currentUser;
  }
  return null;
}

export function isLoggedIn() {
  return isAuthenticated();
}

export async function login(email, password) {
  const data = await apiRequest('/users/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });

  if (data?.status === 'success') {
    setToken(data.access_token);
    localStorage.setItem(USER_EMAIL_KEY, data.email || email);
    _currentUser = { email: data.email || email };
    updateAvatar();
    return { ok: true, message: data.message };
  }

  return { ok: false, message: data?.message || 'Login failed.' };
}

export function logout() {
  _currentUser = null;
  removeToken();
  localStorage.removeItem(USER_EMAIL_KEY);
  localStorage.removeItem('anaida_registration');
  updateAvatar();
}

/* ── Avatar DOM update ── */

export function updateAvatar() {
  const avatar = document.getElementById('navAvatar');
  if (!avatar) return;

  const user = getCurrentUser();
  if (user) {
    const initial = (user.email || '?')[0].toUpperCase();
    avatar.textContent = initial;
    avatar.classList.add('logged-in');
    avatar.title = `Signed in as ${user.email}`;
  } else {
    avatar.textContent = '';
    avatar.classList.remove('logged-in');
    avatar.title = 'Sign in / Register';
  }
}

/* ── Init: called once on page load ── */

export function initAuth() {
  // Restore session from localStorage
  getCurrentUser();
  updateAvatar();

  const avatar = document.getElementById('navAvatar');
  if (!avatar) return;

  avatar.addEventListener('click', () => {
    if (isLoggedIn()) {
      // Show a small logout confirmation
      _showLogoutPrompt(avatar);
    } else {
      // Go to registration/login page
      window.location.href = 'registration.html';
    }
  });
}

/* ── Internal: logout prompt ── */

function _showLogoutPrompt(anchor) {
  // Remove any existing prompt
  const existing = document.getElementById('authPopover');
  if (existing) {
    existing.remove();
    return;
  }

  const user = getCurrentUser();
  const popover = document.createElement('div');
  popover.id = 'authPopover';
  popover.innerHTML = `
    <div class="auth-popover-email">${user?.email || ''}</div>
    <button class="auth-popover-logout" id="logoutBtn">Sign out</button>
  `;
  document.body.appendChild(popover);

  // Position near avatar
  const rect = anchor.getBoundingClientRect();
  popover.style.top = `${rect.bottom + 8}px`;
  popover.style.right = `${window.innerWidth - rect.right}px`;

  document.getElementById('logoutBtn').onclick = () => {
    logout();
    popover.remove();
  };

  // Close on outside click
  setTimeout(() => {
    document.addEventListener('click', function close(e) {
      if (!popover.contains(e.target) && e.target !== anchor) {
        popover.remove();
        document.removeEventListener('click', close);
      }
    });
  }, 0);
}
