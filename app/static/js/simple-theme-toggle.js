/**
 * Simple Theme Toggle - Self-contained working solution
 */

(function() {
    'use strict';
    
    // Theme states
    const THEMES = {
        LIGHT: 'light',
        DARK: 'dark',
        AUTO: 'auto'
    };
    
    let currentTheme = THEMES.LIGHT;
    
    // Initialize theme from localStorage or system preference
    function initTheme() {
        const saved = localStorage.getItem('portfolio-theme');
        if (saved && Object.values(THEMES).includes(saved)) {
            currentTheme = saved;
        } else {
            // Check system preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                currentTheme = THEMES.DARK;
            } else {
                currentTheme = THEMES.LIGHT;
            }
        }
        applyTheme(currentTheme);
    }
    
    // Apply theme to document
    function applyTheme(theme) {
        const html = document.documentElement;
        
        // Remove existing theme
        html.removeAttribute('data-theme');
        
        // Apply new theme
        if (theme === THEMES.DARK) {
            html.setAttribute('data-theme', 'dark');
        } else if (theme === THEMES.AUTO) {
            // For auto, check system preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                html.setAttribute('data-theme', 'dark');
            }
        }
        
        // Update toggle buttons
        updateToggleButtons(theme);
        
        // Save to localStorage
        localStorage.setItem('portfolio-theme', theme);
        
        console.log('Theme applied:', theme);
    }
    
    // Update all toggle buttons
    function updateToggleButtons(theme) {
        const toggles = document.querySelectorAll('.theme-toggle, .theme-toggle-navbar');
        
        toggles.forEach(toggle => {
            const sunIcon = toggle.querySelector('.sun-icon');
            const moonIcon = toggle.querySelector('.moon-icon');
            
            if (sunIcon && moonIcon) {
                if (theme === THEMES.DARK) {
                    sunIcon.style.display = 'block';
                    moonIcon.style.display = 'none';
                } else {
                    sunIcon.style.display = 'none';
                    moonIcon.style.display = 'block';
                }
            }
        });
    }
    
    // Toggle between themes
    function toggleTheme() {
        console.log('Toggling from', currentTheme);
        
        // Cycle through themes
        if (currentTheme === THEMES.LIGHT) {
            currentTheme = THEMES.DARK;
        } else if (currentTheme === THEMES.DARK) {
            currentTheme = THEMES.AUTO;
        } else {
            currentTheme = THEMES.LIGHT;
        }
        
        console.log('Setting theme to:', currentTheme);
        applyTheme(currentTheme);
    }
    
    // Listen for system theme changes
    function watchSystemTheme() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            if (mediaQuery.addEventListener) {
                mediaQuery.addEventListener('change', (e) => {
                    const saved = localStorage.getItem('portfolio-theme');
                    if (saved === THEMES.AUTO || !saved) {
                        applyTheme(THEMES.AUTO);
                    }
                });
            } else if (mediaQuery.addListener) {
                mediaQuery.addListener((e) => {
                    const saved = localStorage.getItem('portfolio-theme');
                    if (saved === THEMES.AUTO || !saved) {
                        applyTheme(THEMES.AUTO);
                    }
                });
            }
        }
    }
    
    // Initialize when DOM is ready
    function init() {
        initTheme();
        watchSystemTheme();
        
        // Make toggle function globally available
        window.toggleThemeDirect = toggleTheme;
        
        console.log('Simple theme toggle initialized with theme:', currentTheme);
    }
    
    // Start initialization
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
