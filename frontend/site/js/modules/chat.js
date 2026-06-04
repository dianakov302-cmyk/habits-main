import { escapeHtml } from './utils.js';
import { apiRequest } from './api.js?v=2';

/* ─────────────────────────────────────────────
   My People — Groups + simulated chat
───────────────────────────────────────────── */

export function initChat() {
  initGroups();
  initMessages();
}

/* ── Groups section ── */

async function initGroups() {
  const groupList  = document.getElementById('groupList');
  const groupInput = document.getElementById('groupInput');
  const groupCreate = document.getElementById('groupCreate');

  if (!groupList) return;

  function renderGroup(group) {
    const card = document.createElement('div');
    card.className = 'group-card';
    card.innerHTML = `
      <div class="group-card-icon">👥</div>
      <div class="group-card-info">
        <div class="group-card-name">${escapeHtml(group.name || 'Unnamed group')}</div>
        <div class="group-card-meta">Community group</div>
      </div>
      <button class="group-join-btn" data-id="${escapeHtml(group.id || group._id || '')}">Join</button>
    `;

    const joinBtn = card.querySelector('.group-join-btn');
    joinBtn?.addEventListener('click', () => {
      joinBtn.textContent = 'Joined ✓';
      joinBtn.disabled = true;
      joinBtn.style.color = 'var(--emerald, #10b981)';
      joinBtn.style.borderColor = 'var(--emerald, #10b981)';
    });

    return card;
  }

  async function loadGroups() {
    try {
      groupList.innerHTML = '<div class="group-loading">Loading groups…</div>';
      const groups = await apiRequest('/groups/');
      groupList.innerHTML = '';

      if (!Array.isArray(groups) || groups.length === 0) {
        groupList.innerHTML = '<div class="group-empty">No groups yet. Create the first one!</div>';
        return;
      }

      groups.forEach(g => groupList.appendChild(renderGroup(g)));
    } catch (_err) {
      groupList.innerHTML = '<div class="group-empty">Could not load groups. Is the server running?</div>';
    }
  }

  if (groupCreate && groupInput) {
    groupCreate.addEventListener('click', async () => {
      const name = groupInput.value.trim();
      if (!name) return;

      groupCreate.disabled = true;
      groupCreate.textContent = '…';
      try {
        await apiRequest('/groups/create', {
          method: 'POST',
          body: JSON.stringify({ name }),
        });
        groupInput.value = '';
        await loadGroups();
      } catch (_err) {
        // optimistic local render on error
        groupList.prepend(renderGroup({ name }));
        groupInput.value = '';
      } finally {
        groupCreate.disabled = false;
        groupCreate.textContent = 'Create';
      }
    });

    groupInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') groupCreate.click();
    });
  }

  loadGroups();
}

/* ── Simulated chat messages ── */

function initMessages() {
  const chatInput = document.getElementById('chatInput');
  const chatSend  = document.getElementById('chatSend');
  const chatList  = document.getElementById('chatList');

  if (!chatInput || !chatSend || !chatList) return;

  const avatars = ['🌿', '⚡', '🔥', '🌙', '💫', '🦋'];
  const replies = [
    'Keep going! 🔥',
    "That's the spirit!",
    'You\'re building something great 💪',
    'One step at a time 🌿',
    'Progress over perfection ✨',
    'Consistency is key 🗝️',
  ];

  function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    const item = document.createElement('div');
    item.className = 'chat-item';
    item.style.justifyContent = 'flex-end';
    item.innerHTML = `<div class="chat-bubble own">${escapeHtml(text)}</div>`;
    chatList.appendChild(item);
    chatInput.value = '';
    chatList.scrollTop = chatList.scrollHeight;

    setTimeout(() => {
      const reply = replies[Math.floor(Math.random() * replies.length)];
      const replyItem = document.createElement('div');
      replyItem.className = 'chat-item';
      replyItem.innerHTML = `
        <div class="chat-avatar">${avatars[Math.floor(Math.random() * avatars.length)]}</div>
        <div class="chat-bubble">${reply}</div>
      `;
      chatList.appendChild(replyItem);
      chatList.scrollTop = chatList.scrollHeight;
    }, 900 + Math.random() * 600);
  }

  chatSend.addEventListener('click', sendMessage);
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') sendMessage();
  });
}
