/**
 * Anaida Space - Main Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Ініціалізація анімації Roadmap при скролі
    initRoadmapAnimation();

    // 2. Логіка перемикання екранів (Nav Pills)
    // Якщо у тебе вже є код для навігації, переконайся, що він не дублюється
    initNavigation();
});

/**
 * Анімація появи карток Roadmap за допомогою Intersection Observer
 */
function initRoadmapAnimation() {
    const steps = document.querySelectorAll('.roadmap-step');

    if (steps.length === 0) return;

    const observerOptions = {
        threshold: 0.15, // спрацює, коли 15% картки з'явиться у в'юпорті
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                // Припиняємо спостерігати після появи
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    steps.forEach(step => {
        observer.observe(step);
    });
}

/**
 * Проста логіка навігації між секціями (Home, Goal, etc.)
 */
function initNavigation() {
    const pills = document.querySelectorAll('.nav-pill');
    const screens = document.querySelectorAll('.screen');

    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            const targetId = pill.getAttribute('data-target');

            // Оновлюємо активну кнопку
            pills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            // Оновлюємо активний екран
            screens.forEach(screen => {
                screen.classList.remove('active');
                if (screen.id === targetId) {
                    screen.classList.add('active');
                    // Скролимо вгору при зміні вкладки
                    screen.scrollTo(0, 0);
                }
            });
        });
    });
}