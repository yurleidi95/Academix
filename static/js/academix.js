/**
 * ACADEMIX - Scripts Globales e Integración de HTMX + Bootstrap 5.3
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Inyección de CSRF Token en peticiones de HTMX
    document.body.addEventListener('htmx:configRequest', function (event) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
                          document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (csrfToken) {
            event.detail.headers['X-CSRFToken'] = csrfToken;
        }
    });

    // 2. Control de Sidebar Colapsable (Móvil / Escritorio)
    const sidebarToggleBtn = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('d-none');
        });
    }

    // 3. Inicialización de Tooltips de Bootstrap 5
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 4. Soporte para eventos disparados por Django mediante cabecera HX-Trigger
    document.body.addEventListener('showMessage', function (evt) {
        const data = evt.detail;
        if (data && data.message) {
            createToast(data.message, data.level || 'info');
        }
    });
});

/**
 * Generador dinámico de Toasts de Bootstrap para respuestas HTMX
 */
function createToast(message, level = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const bgMap = {
        'success': 'bg-success text-white',
        'error': 'bg-danger text-white',
        'danger': 'bg-danger text-white',
        'warning': 'bg-warning text-dark',
        'info': 'bg-primary text-white'
    };
    const toastClass = bgMap[level] || 'bg-secondary text-white';

    const toastHtml = `
        <div class="toast align-items-center ${toastClass} border-0 show shadow" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button>
            </div>
        </div>
    `;

    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = toastHtml.trim();
    const toastEl = tempDiv.firstChild;
    container.appendChild(toastEl);

    setTimeout(() => {
        toastEl.classList.remove('show');
        setTimeout(() => toastEl.remove(), 400);
    }, 4500);
}
