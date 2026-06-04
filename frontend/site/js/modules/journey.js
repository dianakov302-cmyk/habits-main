/**
 * ═══════════════════════ JOURNEY LOGIC ═══════════════════════
 * Handles screen switching, goal selection, and interactivity.
 */

document.addEventListener('DOMContentLoaded', () => {
    const navPills = document.querySelectorAll('.nav-pill');
    const screens = document.querySelectorAll('.screen');
    const goalItems = document.querySelectorAll('.goal-item');

    // 1. СИСТЕМА ПЕРЕМИКАННЯ ЕКРАНІВ
    function switchScreen(targetId) {
        // Прибираємо активний клас з усіх екранів та кнопок
        screens.forEach(screen => screen.classList.remove('active'));
        navPills.forEach(pill => pill.classList.remove('active'));

        // Активуємо потрібний екран
        const targetScreen = document.getElementById(targetId);
        if (targetScreen) {
            targetScreen.classList.add('active');

            // Оновлюємо активну кнопку в меню
            const activePill = document.querySelector(`[data-target="${targetId}"]`);
            if (activePill) activePill.classList.add('active');

            // Прокручуємо вгору при зміні екрану
            targetScreen.scrollTop = 0;
        }
    }

    // Додаємо клік на всі кнопки навігації
    navPills.forEach(pill => {
        pill.addEventListener('click', () => {
            const target = pill.getAttribute('data-target');
            switchScreen(target);
        });
    });

    // 2. ОБРОБКА ВИБОРУ ЦІЛІ (Goal Selection)
    goalItems.forEach(item => {
        item.addEventListener('click', function() {
            // Візуальний ефект вибору
            goalItems.forEach(i => i.style.borderColor = 'rgba(255, 255, 255, 0.05)');
            this.style.borderColor = 'var(--violet)';

            const selectedGoal = this.getAttribute('data-goal');
            const goalName = this.querySelector('.goal-name').innerText;

            console.log(`User selected goal: ${selectedGoal}`);

            // Зберігаємо вибір у LocalStorage (щоб дані не зникали)
            localStorage.setItem('anaida_user_goal', selectedGoal);

            // Перехід до наступного етапу (наприклад, до квізу або тесту)
            setTimeout(() => {
                // Переходимо на окрему сторінку тесту
                window.location.href = 'test.html';
            }, 600); // Коротка затримка для візуального відгуку
        });
    });

    // 3. ІНТЕРАКТИВНІ КНОПКИ (CTA)
    const startJourneyBtn = document.querySelector('.cta-btn');
    if (startJourneyBtn) {
        startJourneyBtn.addEventListener('click', (e) => {
            e.preventDefault();
            switchScreen('goal'); // Ведемо користувача відразу до вибору цілі
        });
    }

    const openQuizBtn = document.getElementById('openQuiz');
    if (openQuizBtn) {
        openQuizBtn.addEventListener('click', () => {
            window.location.href = 'test.html';
        });
    }

    // 4. ПЕРЕВІРКА СТАНУ ПРИ ЗАВАНТАЖЕННІ
    // Якщо користувач вже вибирав ціль, ми можемо це відобразити
    const savedGoal = localStorage.getItem('anaida_user_goal');
    if (savedGoal) {
        const activeGoalItem = document.querySelector(`[data-goal="${savedGoal}"]`);
        if (activeGoalItem) {
            activeGoalItem.style.borderColor = 'var(--violet)';
            activeGoalItem.style.background = 'rgba(139, 92, 246, 0.1)';
        }
    }
});

// Додатковий ефект для "дорогого" вигляду: Паралакс фону при русі миші
document.addEventListener('mousemove', (e) => {
    const moveX = (e.clientX - window.innerWidth / 2) * 0.01;
    const moveY = (e.clientY - window.innerHeight / 2) * 0.01;

    const activeScreen = document.querySelector('.screen.active');
    if (activeScreen) {
        activeScreen.style.backgroundPosition = `${50 + moveX}% ${50 + moveY}%`;
    }
});
