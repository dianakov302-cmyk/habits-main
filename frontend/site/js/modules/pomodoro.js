export function initPomodoro() {
  const display = document.getElementById('timerDisplay');
  const startBtn = document.getElementById('startBtn');
  const resetBtn = document.getElementById('resetBtn');
  const stateLabel = document.getElementById('pomodoroState');
  const timeModal = document.getElementById('timeModal');
  const modalTitle = document.getElementById('modalTitle');
  const modalInput = document.getElementById('modalInput');
  const modalConfirm = document.getElementById('modalConfirm');
  const modalCancel = document.getElementById('modalCancel');
  const ring = document.getElementById('pomodoroRing');

  if (!display || !startBtn || !resetBtn || !stateLabel || !timeModal || !modalTitle || !modalInput || !modalConfirm || !modalCancel) {
    return;
  }

  let focusMinutes = 25;
  let breakMinutes = 5;
  let remaining = focusMinutes * 60;
  let interval = null;
  let isRunning = false;
  let isFocusPhase = true;
  let currentModalTarget = 'time';
  const CIRCUMFERENCE = 2 * Math.PI * 98;

  function formatTime(s) {
    const minutes = Math.floor(s / 60).toString().padStart(2, '0');
    const seconds = (s % 60).toString().padStart(2, '0');
    return `${minutes}:${seconds}`;
  }

  function updateRing() {
    if (!ring) return;
    const total = (isFocusPhase ? focusMinutes : breakMinutes) * 60;
    const pct = remaining / total;
    ring.style.strokeDashoffset = CIRCUMFERENCE * (1 - pct);
    ring.classList.toggle('break-phase', !isFocusPhase);
  }

  function updateDisplay() {
    display.textContent = formatTime(remaining);
    document.title = `${formatTime(remaining)} — Anaida Space`;
    updateRing();
  }

  function startTimer() {
    clearInterval(interval);
    interval = setInterval(tick, 1000);
    isRunning = true;
    startBtn.textContent = 'Pause';
  }

  function tick() {
    if (remaining <= 0) {
      clearInterval(interval);
      isRunning = false;
      startBtn.textContent = 'Start';
      switchPhase();
      return;
    }
    remaining--;
    updateDisplay();
  }

  function switchPhase() {
    isFocusPhase = !isFocusPhase;
    if (isFocusPhase) {
      remaining = focusMinutes * 60;
      stateLabel.textContent = 'Focus Time';
      display.style.color = 'rgba(255,255,255,.92)';
    } else {
      remaining = breakMinutes * 60;
      stateLabel.textContent = 'Break Time 🌿';
      display.style.color = '#10b981';
    }
    updateDisplay();
    startTimer();
  }

  startBtn.addEventListener('click', () => {
    if (isRunning) {
      clearInterval(interval);
      isRunning = false;
      startBtn.textContent = 'Start';
      return;
    }
    startTimer();
  });

  resetBtn.addEventListener('click', () => {
    clearInterval(interval);
    isRunning = false;
    isFocusPhase = true;
    remaining = focusMinutes * 60;
    startBtn.textContent = 'Start';
    stateLabel.textContent = 'Focus Time';
    display.style.color = 'rgba(255,255,255,.92)';
    updateDisplay();
    document.title = 'Anaida Space — Break the Circle';
    if (ring) {
      ring.style.strokeDashoffset = 0;
      ring.classList.remove('break-phase');
    }
  });

  document.getElementById('changeTimeBtn')?.addEventListener('click', () => {
    currentModalTarget = 'time';
    modalTitle.textContent = 'Set Focus Time (minutes)';
    modalInput.value = focusMinutes;
    timeModal.classList.add('open');
  });

  document.getElementById('changeBreakBtn')?.addEventListener('click', () => {
    currentModalTarget = 'break';
    modalTitle.textContent = 'Set Break Time (minutes)';
    modalInput.value = breakMinutes;
    timeModal.classList.add('open');
  });

  modalConfirm.addEventListener('click', () => {
    const val = parseInt(modalInput.value, 10);
    if (Number.isNaN(val) || val < 1) return;
    if (currentModalTarget === 'time') {
      focusMinutes = val;
      if (isFocusPhase) {
        remaining = val * 60;
        updateDisplay();
      }
    } else {
      breakMinutes = val;
      if (!isFocusPhase) {
        remaining = val * 60;
        updateDisplay();
      }
    }
    timeModal.classList.remove('open');
  });

  modalCancel.addEventListener('click', () => timeModal.classList.remove('open'));
  timeModal.addEventListener('click', event => {
    if (event.target === timeModal) timeModal.classList.remove('open');
  });

  updateDisplay();
}
