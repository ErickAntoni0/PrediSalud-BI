// ===== MODO OSCURO - SISTEMA MÉDICO BI =====

class DarkModeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Aplicar tema inicial
        this.applyTheme();
        
        // Crear botón de toggle si no existe
        this.createToggleButton();
        
        // Escuchar cambios en el sistema
        this.listenForSystemChanges();
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        localStorage.setItem('theme', this.theme);
        
        // Actualizar icono del botón
        this.updateToggleIcon();
        
        // Disparar evento personalizado
        document.dispatchEvent(new CustomEvent('themeChanged', { 
            detail: { theme: this.theme } 
        }));
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme();
        
        // Animación suave
        this.animateTransition();
    }

    createToggleButton() {
        // Verificar si ya existe el botón
        if (document.querySelector('.theme-toggle')) {
            return;
        }

        const toggleButton = document.createElement('button');
        toggleButton.className = 'theme-toggle';
        toggleButton.setAttribute('aria-label', 'Cambiar modo oscuro');
        toggleButton.setAttribute('title', 'Cambiar modo oscuro');
        
        // Agregar icono inicial
        this.updateToggleIcon(toggleButton);
        
        // Agregar evento click
        toggleButton.addEventListener('click', () => {
            this.toggleTheme();
        });

        // Agregar al body
        document.body.appendChild(toggleButton);
    }

    updateToggleIcon(button = null) {
        const toggleButton = button || document.querySelector('.theme-toggle');
        if (!toggleButton) return;

        const icon = this.theme === 'light' ? '🌙' : '☀️';
        toggleButton.innerHTML = icon;
        toggleButton.setAttribute('title', 
            this.theme === 'light' ? 'Activar modo oscuro' : 'Activar modo claro'
        );
    }

    animateTransition() {
        // Agregar clase de transición
        document.body.classList.add('theme-transitioning');
        
        // Remover después de la transición
        setTimeout(() => {
            document.body.classList.remove('theme-transitioning');
        }, 300);
    }

    listenForSystemChanges() {
        // Escuchar cambios en las preferencias del sistema
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            mediaQuery.addEventListener('change', (e) => {
                // Solo cambiar si el usuario no ha establecido una preferencia manual
                if (!localStorage.getItem('theme')) {
                    this.theme = e.matches ? 'dark' : 'light';
                    this.applyTheme();
                }
            });
        }
    }

    // Método para obtener el tema actual
    getCurrentTheme() {
        return this.theme;
    }

    // Método para establecer tema específico
    setTheme(theme) {
        if (['light', 'dark'].includes(theme)) {
            this.theme = theme;
            this.applyTheme();
        }
    }

    // Método para verificar si está en modo oscuro
    isDarkMode() {
        return this.theme === 'dark';
    }
}

// Función para inicializar el modo oscuro
function initDarkMode() {
    // Crear instancia global
    window.darkModeManager = new DarkModeManager();
    
    // Agregar estilos de transición
    const style = document.createElement('style');
    style.textContent = `
        .theme-transitioning * {
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
        }
        
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: var(--accent-color);
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            box-shadow: 0 2px 10px var(--shadow-color);
            transition: all 0.3s ease;
        }
        
        .theme-toggle:hover {
            background: var(--accent-hover);
            transform: scale(1.1);
        }
        
        .theme-toggle:focus {
            outline: 2px solid var(--accent-color);
            outline-offset: 2px;
        }
    `;
    document.head.appendChild(style);
}

// Función para agregar el botón de toggle a una posición específica
function addThemeToggleToElement(selector) {
    const element = document.querySelector(selector);
    if (!element) return;

    const toggleButton = document.createElement('button');
    toggleButton.className = 'theme-toggle-inline';
    toggleButton.setAttribute('aria-label', 'Cambiar modo oscuro');
    toggleButton.setAttribute('title', 'Cambiar modo oscuro');
    
    // Estilos inline para el botón
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
    `;
    
    // Agregar icono
    const currentTheme = window.darkModeManager?.getCurrentTheme() || 'light';
    toggleButton.innerHTML = currentTheme === 'light' ? '🌙' : '☀️';
    
    // Agregar evento click
    toggleButton.addEventListener('click', () => {
        if (window.darkModeManager) {
            window.darkModeManager.toggleTheme();
            // Actualizar icono
            toggleButton.innerHTML = window.darkModeManager.isDarkMode() ? '☀️' : '🌙';
        }
    });
    
    element.appendChild(toggleButton);
}

// Función para agregar toggle al header
function addThemeToggleToHeader() {
    const header = document.querySelector('.header, .navbar, .nav');
    if (header) {
        addThemeToggleToElement('.header-content, .navbar-nav, .nav');
    }
}

// Función para agregar toggle al sidebar
function addThemeToggleToSidebar() {
    const sidebar = document.querySelector('.sidebar, .nav-sidebar');
    if (sidebar) {
        addThemeToggleToElement('.sidebar, .nav-sidebar');
    }
}

// Función para agregar toggle al footer
function addThemeToggleToFooter() {
    const footer = document.querySelector('.footer');
    if (footer) {
        addThemeToggleToElement('.footer');
    }
}

// Función para detectar automáticamente la preferencia del sistema
function detectSystemPreference() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }
    return 'light';
}

// Función para aplicar tema automáticamente basado en la hora del día
function applyTimeBasedTheme() {
    const hour = new Date().getHours();
    const isNight = hour < 6 || hour >= 18;
    
    if (isNight && !localStorage.getItem('theme')) {
        window.darkModeManager?.setTheme('dark');
    }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDarkMode);
} else {
    initDarkMode();
}

// Exportar funciones para uso global
window.DarkModeUtils = {
    init: initDarkMode,
    addToHeader: addThemeToggleToHeader,
    addToSidebar: addThemeToggleToSidebar,
    addToFooter: addThemeToggleToFooter,
    detectSystemPreference,
    applyTimeBasedTheme
};

// Ejemplo de uso:
// 
// // Inicializar modo oscuro
// initDarkMode();
// 
// // Agregar toggle al header
// addThemeToggleToHeader();
// 
// // Aplicar tema basado en la hora
// applyTimeBasedTheme();
// 
// // Detectar preferencia del sistema
// const systemTheme = detectSystemPreference();
// console.log('Tema del sistema:', systemTheme); 