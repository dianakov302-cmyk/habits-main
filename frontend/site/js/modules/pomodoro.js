let pomodoroReady = false;

export function initPomodoro() {
  if (pomodoroReady) return;

  const display = document.getElementById('timerDisplay');
  const startBtn = document.getElementById('startBtn');
  const resetBtn = document.getElementById('resetBtn');
  const stateLabel = document.getElementById('pomodoroState');
  const timeModal = document.getElementById('timeModal');
  const modalTitle = document.getElementById('modalTitle');
  const modalInput = document.getElementById('modalInput');
  const modalConfirm = document.getElementById('modalConfirm');
  const modalCancel = document.getElementById('modalCancel');
  const animal = document.getElementById('pomodoroAnimal');
  const circleProgress = document.getElementById('pomCircleProgress');
  if (!display || !startBtn || !resetBtn || !stateLabel || !timeModal) {
    return;
  }

  pomodoroReady = true;

  let focusMinutes = 25;
  let breakMinutes = 5;
  let remaining = focusMinutes * 60;
  let interval = null;
  let isRunning = false;
  let isFocusPhase = true;
  let currentModalTarget = 'time';
  const CIRCUMFERENCE = 282.7;

  function formatTime(s) {
    const minutes = Math.floor(s / 60).toString().padStart(2, '0');
    const seconds = (s % 60).toString().padStart(2, '0');
    return `${minutes}:${seconds}`;
  }

  function updateDisplay() {
    const text = formatTime(remaining);
    display.textContent = text;
    document.title = isRunning ? `${text} — Anaida Space` : 'Anaida Space';
    updateRing();
  }

  function updateRing() {
    const total = (isFocusPhase ? focusMinutes : breakMinutes) * 60;
    const pct = total > 0 ? Math.max(0, remaining / total) : 0;
    if (circleProgress) {
      circleProgress.style.strokeDashoffset = CIRCUMFERENCE * (1 - pct);
    }
  }

  function updateAnimal() {
    if (!animal) return;
    animal.classList.remove('breathing', 'focusing', 'breaking');

    if (!isRunning) {
      animal.classList.add('breathing');
    } else if (isFocusPhase) {
      animal.classList.add('focusing');
    } else {
      animal.classList.add('breaking');
    }
  }

  function startTimer() {
    if (interval) clearInterval(interval);
    interval = setInterval(tick, 1000);
    isRunning = true;
    startBtn.textContent = '⏸ Pause';
    updateAnimal();
    updateDisplay();
  }

  function pauseTimer() {
    clearInterval(interval);
    interval = null;
    isRunning = false;
    startBtn.textContent = '▶ Start';
    updateAnimal();
    document.title = 'Anaida Space';
  }

  function tick() {
    if (remaining <= 0) {
      clearInterval(interval);
      interval = null;
      isRunning = false;
      startBtn.textContent = '▶ Start';
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
      stateLabel.textContent = 'FOCUS';
      stateLabel.style.color = '#8b5cf6';
      display.style.color = 'rgba(255,255,255,.92)';
    } else {
      remaining = breakMinutes * 60;
      stateLabel.textContent = 'BREAK';
      stateLabel.style.color = '#10b981';
      display.style.color = '#10b981';
    }
    updateDisplay();
    updateAnimal();
    startTimer();
  }

  startBtn.addEventListener('click', () => {
    if (isRunning) pauseTimer();
    else startTimer();
  });

  resetBtn.addEventListener('click', () => {
    clearInterval(interval);
    interval = null;
    isRunning = false;
    isFocusPhase = true;
    remaining = focusMinutes * 60;
    startBtn.textContent = '▶ Start';
    stateLabel.textContent = 'FOCUS';
    stateLabel.style.color = '#8b5cf6';
    display.style.color = 'rgba(255,255,255,.92)';
    updateDisplay();
    updateAnimal();
    document.title = 'Anaida Space';
  });

  document.getElementById('changeTimeBtn')?.addEventListener('click', () => {
    currentModalTarget = 'time';
    modalTitle.textContent = 'Set Focus Time (minutes)';
    modalInput.value = focusMinutes;
    timeModal.classList.add('open');
    modalInput.focus();
  });

  document.getElementById('changeBreakBtn')?.addEventListener('click', () => {
    currentModalTarget = 'break';
    modalTitle.textContent = 'Set Break Time (minutes)';
    modalInput.value = breakMinutes;
    timeModal.classList.add('open');
    modalInput.focus();
  });

  modalConfirm.addEventListener('click', () => {
    const val = parseInt(modalInput.value, 10);
    if (Number.isNaN(val) || val < 1) return;

    if (currentModalTarget === 'time') {
      focusMinutes = val;
      const focusDisplay = document.getElementById('focusMinDisplay');
      if (focusDisplay) focusDisplay.textContent = val;
      if (isFocusPhase && !isRunning) {
        remaining = val * 60;
        updateDisplay();
      }
    } else {
      breakMinutes = val;
      const breakDisplay = document.getElementById('breakMinDisplay');
      if (breakDisplay) breakDisplay.textContent = val;
      if (!isFocusPhase && !isRunning) {
        remaining = val * 60;
        updateDisplay();
      }
    }
    timeModal.classList.remove('open');
  });

  modalCancel.addEventListener('click', () => timeModal.classList.remove('open'));
  modalInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') modalConfirm.click();
    if (e.key === 'Escape') modalCancel.click();
  });
  timeModal.addEventListener('click', (event) => {
    if (event.target === timeModal) timeModal.classList.remove('open');
  });

  updateDisplay();
  updateAnimal();
}
