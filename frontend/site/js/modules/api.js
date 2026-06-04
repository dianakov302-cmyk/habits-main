import './article-tab.js';

const DEFAULT_API_BASE_URL = 'http://localhost:8080';

export const USER_EMAIL_KEY = 'anaida_user_email';
const TOKEN_KEY = 'anaida_token';

function getApiBaseUrl() {
  const configured = window.localStorage.getItem('anaida_api_base_url');
  if (configured && typeof configured === 'string') {
    return configured.replace(/\/+$/, '');
  }
  return DEFAULT_API_BASE_URL;
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export function isAuthenticated() {
  return !!getToken();
}

export async function apiRequest(path, options = {}) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  const url = `${getApiBaseUrl()}${normalizedPath}`;

  console.log(`API Request: ${options.method || 'GET'} ${url}`);

  const token = getToken();
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;
  // Allow caller to override/extend headers
  Object.assign(headers, options.headers || {});

  const response = await fetch(url, {
    ...options,
    headers,
  });

  console.log(`API Response: ${response.status} from ${url}`);

  // Handle 401: only redirect if we actually sent a token (user was supposed to be authenticated)
  // Don't redirect on public pages that make unauthenticated requests
  if (response.status === 401 && token) {
    removeToken();
    localStorage.removeItem(USER_EMAIL_KEY);
    window.location.href = 'registration.html';
    return;
  }

  let data = null;
  try {
    data = await response.json();
  } catch (_error) {
    data = null;
  }

  if (!response.ok) {
    const message = data?.message || `Request failed with status ${response.status}`;
    throw new Error(message);
  }

  return data;
}
