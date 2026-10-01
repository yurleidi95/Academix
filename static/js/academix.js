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

/**
 * 6. Validación Global de Campos Numéricos Estrictos (Solo Números)
 * Impide escribir, tipear o pegar letras, símbolos, signos o espacios en campos de numeración.
 */
function isNumericInputField(el) {
    if (!el || el.tagName !== 'INPUT') return false;
    const type = (el.getAttribute('type') || 'text').toLowerCase();
    if (['checkbox', 'radio', 'file', 'submit', 'button', 'color', 'date', 'datetime-local', 'password'].includes(type)) {
        return false;
    }

    // Excluir inputs de notas con decimales (p.ej. calificaciones 1.0 a 5.0)
    if (el.classList.contains('grade-cell-input') || el.classList.contains('grade-input') || el.getAttribute('inputmode') === 'decimal' || el.getAttribute('step')) {
        return false;
    }

    const name = (el.getAttribute('name') || '').toLowerCase();
    const id = (el.getAttribute('id') || '').toLowerCase();
    const inputMode = (el.getAttribute('inputmode') || '').toLowerCase();
    const pattern = el.getAttribute('pattern') || '';

    if (el.classList.contains('only-numbers') || el.dataset.onlyNumbers === 'true') return true;
    if (inputMode === 'numeric' && (pattern.includes('[0-9]') || pattern === '[0-9]*')) return true;
    if (type === 'number' && !el.getAttribute('step')) return true;

    const numericNames = [
        'document_number', 'phone', 'telefono', 'celular', 'doc_num', 'cedula',
        'student_code', 'student_id_target', 'capacity', 'student_id'
    ];

    return numericNames.some(item => name === item || name.endsWith('[' + item + ']') || id.includes(item));
}

// Bloqueo en tiempo real de teclas no numéricas
document.addEventListener('keydown', function (e) {
    if (!isNumericInputField(e.target)) return;

    // Permitir teclas de navegación y control del sistema
    const allowedKeys = [
        'Backspace', 'Delete', 'Tab', 'Escape', 'Enter',
        'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'
    ];
    if (allowedKeys.includes(e.key)) return;

    // Permitir atajos (Ctrl+A, Ctrl+C, Ctrl+V, etc.)
    if (e.ctrlKey || e.metaKey) return;

    // Si no es un dígito del 0 al 9, bloquear el evento
    if (!/^[0-9]$/.test(e.key)) {
        e.preventDefault();
    }
}, true);

// Limpieza reactiva ante inputs (autocompletado, reconocimiento de voz o arrastre de texto)
document.addEventListener('input', function (e) {
    if (isNumericInputField(e.target)) {
        const originalVal = e.target.value;
        const cleanVal = originalVal.replace(/[^0-9]/g, '');
        if (originalVal !== cleanVal) {
            e.target.value = cleanVal;
        }
    }
}, true);

// Bloqueo y saneamiento automático al pegar contenido desde el portapapeles
document.addEventListener('paste', function (e) {
    if (isNumericInputField(e.target)) {
        e.preventDefault();
        const text = (e.clipboardData || window.clipboardData).getData('text') || '';
        const cleanText = text.replace(/[^0-9]/g, '');
        if (cleanText) {
            const target = e.target;
            const start = target.selectionStart || 0;
            const end = target.selectionEnd || 0;
            const val = target.value;
            target.value = val.slice(0, start) + cleanText + val.slice(end);
            target.setSelectionRange(start + cleanText.length, start + cleanText.length);
            target.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
}, true);

