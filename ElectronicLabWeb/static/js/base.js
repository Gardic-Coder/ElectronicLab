/*document.addEventListener('DOMContentLoaded', () => {

    const html = document.documentElement;
    const toggleBtn = document.querySelector('.theme-toggle');
    const icon = toggleBtn.querySelector('i');

    // Cargar preferencia guardada
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        html.setAttribute('data-bs-theme', savedTheme);
        icon.className = savedTheme === 'dark' ? 'bi bi-moon text-warning' : 'bi bi-brightness-high text-warning';
    }

    // Cambiar tema y guardar preferencia
    toggleBtn.addEventListener('click', () => {
        const current = html.getAttribute('data-bs-theme');
        const next = current === 'light' ? 'dark' : 'light';
        html.setAttribute('data-bs-theme', next);
        localStorage.setItem('theme', next);
        icon.className = next === 'dark' ? 'bi bi-moon text-warning' : 'bi bi-brightness-high text-warning';
    });
});*/
document.addEventListener('DOMContentLoaded', () => {
    const html = document.documentElement;
    const toggleButtons = document.querySelectorAll('.theme-toggle');

    const updateTheme = (theme) => {
        html.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        toggleButtons.forEach(btn => {
            const icon = btn.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'bi bi-moon text-warning' : 'bi bi-brightness-high text-warning';
            }
        });
    };

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        updateTheme(savedTheme);
    }

    toggleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const current = html.getAttribute('data-bs-theme');
            const next = current === 'light' ? 'dark' : 'light';
            updateTheme(next);
        });
    });
});