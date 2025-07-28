// ===== APLICAR MODO OSCURO A TODAS LAS PLANTILLAS =====

// Función para aplicar modo oscuro a cualquier plantilla
function applyDarkModeToTemplate() {
    // Verificar si ya se aplicó
    if (document.querySelector('.dark-mode-applied')) {
        return;
    }

    // Agregar CSS del modo oscuro si no existe
    if (!document.querySelector('link[href*="dark-mode.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/static/css/dark-mode.css';
        document.head.appendChild(link);
    }

    // Agregar script del modo oscuro si no existe
    if (!document.querySelector('script[src*="dark-mode.js"]')) {
        const script = document.createElement('script');
        script.src = '/static/js/dark-mode.js';
        script.onload = function() {
            if (window.DarkModeUtils) {
                window.DarkModeUtils.init();
                window.DarkModeUtils.applyTimeBasedTheme();
                console.log('Modo oscuro aplicado automáticamente');
            }
        };
        document.head.appendChild(script);
    }

    // Marcar como aplicado
    document.body.classList.add('dark-mode-applied');
}

// Función para aplicar estilos específicos según el tipo de plantilla
function applyTemplateSpecificStyles() {
    const currentPage = window.location.pathname;
    
    // Detectar tipo de plantilla
    if (currentPage.includes('login')) {
        applyLoginStyles();
    } else if (currentPage.includes('dashboard')) {
        applyDashboardStyles();
    } else if (currentPage.includes('registro')) {
        applyRegistroStyles();
    } else {
        applyGenericStyles();
    }
}

// Estilos específicos para login
function applyLoginStyles() {
    const style = document.createElement('style');
    style.textContent = `
        [data-theme="dark"] body::before {
            background-color: rgba(0, 0, 0, 0.7) !important;
        }
        
        [data-theme="dark"] .container {
            background-color: var(--bg-primary) !important;
        }
        
        [data-theme="dark"] .container button {
            background-color: var(--accent-color) !important;
        }
        
        [data-theme="dark"] .container button.ghost {
            border-color: var(--text-primary) !important;
            color: var(--text-primary) !important;
        }
    `;
    document.head.appendChild(style);
}

// Estilos específicos para dashboard
function applyDashboardStyles() {
    const style = document.createElement('style');
    style.textContent = `
        [data-theme="dark"] body {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        }
        
        [data-theme="dark"] .header {
            background: rgba(45, 45, 45, 0.95) !important;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3) !important;
        }
        
        [data-theme="dark"] .logo {
            color: var(--text-primary) !important;
        }
        
        [data-theme="dark"] .user-name {
            color: var(--text-primary) !important;
        }
        
        [data-theme="dark"] .user-role {
            color: var(--text-secondary) !important;
        }
        
        [data-theme="dark"] .card {
            background-color: var(--bg-secondary) !important;
            border: 1px solid var(--border-color) !important;
        }
        
        [data-theme="dark"] .card h3 {
            color: var(--text-primary) !important;
        }
        
        [data-theme="dark"] .card p {
            color: var(--text-secondary) !important;
        }
    `;
    document.head.appendChild(style);
}

// Estilos específicos para registro
function applyRegistroStyles() {
    const style = document.createElement('style');
    style.textContent = `
        [data-theme="dark"] body {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        }
        
        [data-theme="dark"] .container {
            background: var(--bg-primary) !important;
            box-shadow: 0 25px 50px var(--shadow-color) !important;
        }
        
        [data-theme="dark"] .header {
            background: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-hover) 100%) !important;
        }
        
        [data-theme="dark"] .form-section {
            background-color: var(--bg-secondary) !important;
        }
        
        [data-theme="dark"] .form-section h3 {
            color: var(--text-primary) !important;
        }
        
        [data-theme="dark"] .form-group label {
            color: var(--text-primary) !important;
        }
        
        [data-theme="dark"] .form-control {
            background-color: var(--bg-tertiary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }
        
        [data-theme="dark"] .form-control:focus {
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
        }
        
        [data-theme="dark"] .btn-primary {
            background-color: var(--accent-color) !important;
            color: white !important;
        }
        
        [data-theme="dark"] .btn-primary:hover {
            background-color: var(--accent-hover) !important;
        }
    `;
    document.head.appendChild(style);
}

// Estilos genéricos para otras plantillas
function applyGenericStyles() {
    const style = document.createElement('style');
    style.textContent = `
        [data-theme="dark"] body {
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }
        
        [data-theme="dark"] .container {
            background-color: var(--bg-primary) !important;
        }
        
        [data-theme="dark"] .header, [data-theme="dark"] .navbar {
            background-color: var(--bg-secondary) !important;
            border-bottom: 1px solid var(--border-color) !important;
        }
        
        [data-theme="dark"] .card, [data-theme="dark"] .panel {
            background-color: var(--bg-secondary) !important;
            border: 1px solid var(--border-color) !important;
        }
        
        [data-theme="dark"] input, [data-theme="dark"] textarea, [data-theme="dark"] select {
            background-color: var(--bg-tertiary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }
        
        [data-theme="dark"] .btn {
            background-color: var(--accent-color) !important;
            color: white !important;
        }
        
        [data-theme="dark"] .btn:hover {
            background-color: var(--accent-hover) !important;
        }
    `;
    document.head.appendChild(style);
}

// Función para aplicar modo oscuro automáticamente
function autoApplyDarkMode() {
    // Esperar a que el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            applyDarkModeToTemplate();
            applyTemplateSpecificStyles();
        });
    } else {
        applyDarkModeToTemplate();
        applyTemplateSpecificStyles();
    }
}

// Función para aplicar modo oscuro a plantillas específicas
function applyDarkModeToSpecificTemplates() {
    const templates = [
        'login_integrated.html',
        'dashboard_mejorado.html',
        'registro.html',
        'login.html',
        'dashboard.html',
        'index.html',
        'about.html',
        'contact.html',
        'service.html',
        'doctor.html',
        'department.html',
        'appoinment.html',
        'blog-single.html',
        'blog-sidebar.html',
        'confirmation.html',
        'doctor-single.html',
        'department-single.html'
    ];

    const currentPage = window.location.pathname.split('/').pop();
    
    if (templates.includes(currentPage)) {
        autoApplyDarkMode();
    }
}

// Función para aplicar modo oscuro a todas las plantillas
function applyDarkModeToAllTemplates() {
    // Aplicar automáticamente
    autoApplyDarkMode();
    
    // También aplicar a plantillas específicas
    applyDarkModeToSpecificTemplates();
}

// Función para agregar toggle a cualquier plantilla
function addThemeToggleToAnyTemplate() {
    // Buscar elementos donde agregar el toggle
    const possibleSelectors = [
        '.header-content',
        '.navbar-nav',
        '.nav',
        '.header',
        '.navbar',
        '.sidebar',
        '.nav-sidebar',
        '.footer',
        '.container',
        'body'
    ];

    for (const selector of possibleSelectors) {
        const element = document.querySelector(selector);
        if (element) {
            // Crear botón de toggle
            const toggleButton = document.createElement('button');
            toggleButton.className = 'theme-toggle-inline';
            toggleButton.setAttribute('aria-label', 'Cambiar modo oscuro');
            toggleButton.setAttribute('title', 'Cambiar modo oscuro');
            
            // Estilos inline
            toggleButton.style.cssText = `
                background: var(--accent-color);
                color: white;
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1rem;
                transition: all 0.3s ease;
                margin-left: 10px;
                position: relative;
                z-index: 1000;
            `;
            
            // Agregar icono
            const currentTheme = localStorage.getItem('theme') || 'light';
            toggleButton.innerHTML = currentTheme === 'light' ? '🌙' : '☀️';
            
            // Agregar evento click
            toggleButton.addEventListener('click', () => {
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                localStorage.setItem('theme', newTheme);
                document.documentElement.setAttribute('data-theme', newTheme);
                toggleButton.innerHTML = newTheme === 'light' ? '🌙' : '☀️';
                
                // Recargar estilos
                applyTemplateSpecificStyles();
            });
            
            element.appendChild(toggleButton);
            break;
        }
    }
}

// Función para inicializar todo
function initDarkModeForAllTemplates() {
    // Aplicar modo oscuro
    applyDarkModeToAllTemplates();
    
    // Agregar toggle
    setTimeout(() => {
        addThemeToggleToAnyTemplate();
    }, 1000);
}

// Ejecutar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDarkModeForAllTemplates);
} else {
    initDarkModeForAllTemplates();
}

// Exportar funciones para uso global
window.DarkModeAutoApply = {
    applyToTemplate: applyDarkModeToTemplate,
    applyToAllTemplates: applyDarkModeToAllTemplates,
    addToggle: addThemeToggleToAnyTemplate,
    init: initDarkModeForAllTemplates
};

console.log('Script de modo oscuro automático cargado'); 