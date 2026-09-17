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

    // 5. Efecto de Desenfoque y Enfoque al Interactuar con Formularios y Módulos
    const overlay = document.getElementById('ac-focus-overlay');
    let currentElevated = null;

    function activateFocusBlur(element) {
        if (!overlay || !element) return;
        if (currentElevated && currentElevated !== element) {
            currentElevated.classList.remove('ac-focus-elevated');
        }
        currentElevated = element;
        element.classList.add('ac-focus-elevated');
        overlay.classList.add('active');
    }

    function deactivateFocusBlur() {
        if (currentElevated) {
            currentElevated.classList.remove('ac-focus-elevated');
            currentElevated = null;
        }
        if (overlay) {
            overlay.classList.remove('active');
        }
    }

    if (overlay) {
        overlay.addEventListener('click', deactivateFocusBlur);
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') deactivateFocusBlur();
        });
    }

    // Auto-activación al enfocar en formularios o tablas de calificación interactiva
    document.addEventListener('focusin', function (e) {
        const target = e.target;
        if (target.matches('#bulkGradeForm input, #bulkGradeForm select, .ac-focus-form input, .ac-focus-form select, .ac-focus-form textarea')) {
            const card = target.closest('.ac-card') || target.closest('form');
            if (card) activateFocusBlur(card);
        }
    });

    document.addEventListener('click', function (e) {
        const target = e.target;
        if (overlay && overlay.classList.contains('active')) {
            if (!target.closest('.ac-focus-elevated') && !target.closest('.modal')) {
                deactivateFocusBlur();
            }
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
