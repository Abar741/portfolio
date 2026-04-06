/**
 * Theme Management System
 * Handles dark/light mode toggling with localStorage persistence
 * and respects system preferences
 */

class ThemeManager {
    constructor() {
        this STORAGE_KEY = 'portfolio-theme';
        this.THEME_DARK = 'dark';
        this.THEME_LIGHT = 'light';
        this.THEME_AUTO = 'auto';
        
        this.init();
    }
    
    /**
     * Initialize theme system
     */
    init() {
        // Set initial theme based on saved preference or system preference
        const savedTheme = this.getSavedTheme();
        const systemTheme = this.getSystemTheme();
        
        if (savedTheme && savedTheme !== this.THEME_AUTO) {
            this.setTheme(savedTheme);
        } else if (savedTheme === this.THEME_AUTO || !savedTheme) {
            this.setTheme(systemTheme);
        }
        
        // Listen for system theme changes
        this.watchSystemTheme();
        
        // Add theme toggle to DOM
        this.addThemeToggle();
    }
    
    /**
     * Get saved theme from localStorage
     */
    getSavedTheme() {
        try {
            return localStorage.getItem(this.STORAGE_KEY);
        } catch (e) {
            console.warn('Could not read theme from localStorage:', e);
            return null;
        }
    }
    
    /**
     * Save theme to localStorage
     */
    saveTheme(theme) {
        try {
            localStorage.setItem(this.STORAGE_KEY, theme);
        } catch (e) {
            console.warn('Could not save theme to localStorage:', e);
        }
    }
    
    /**
     * Get system preferred theme
     */
    getSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return this.THEME_DARK;
        }
        return this.THEME_LIGHT;
    }
    
    /**
     * Watch for system theme changes
     */
    watchSystemTheme() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            // Modern browsers support addEventListener
            if (mediaQuery.addEventListener) {
                mediaQuery.addEventListener('change', (e) => {
                    const savedTheme = this.getSavedTheme();
                    if (savedTheme === this.THEME_AUTO || !savedTheme) {
                        this.setTheme(e.matches ? this.THEME_DARK : this.THEME_LIGHT);
                    }
                });
            }
            // Fallback for older browsers
            else if (mediaQuery.addListener) {
                mediaQuery.addListener((e) => {
                    const savedTheme = this.getSavedTheme();
                    if (savedTheme === this.THEME_AUTO || !savedTheme) {
                        this.setTheme(e.matches ? this.THEME_DARK : this.THEME_LIGHT);
                    }
                });
            }
        }
    }
    
    /**
     * Set theme on document
     */
    setTheme(theme) {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme');
        
        console.log('Theme Manager: Setting theme', theme, 'current:', currentTheme);
        
        if (currentTheme === theme) {
            console.log('Theme Manager: Theme already set, skipping');
            return; // Theme is already set
        }
        
        // Remove existing theme attribute
        html.removeAttribute('data-theme');
        
        // Set new theme attribute
        if (theme !== this.THEME_LIGHT) {
            html.setAttribute('data-theme', theme);
        }
        
        console.log('Theme Manager: Theme attribute set to', html.getAttribute('data-theme') || 'light');
        
        // Update toggle button
        this.updateToggleButton(theme);
        
        // Save preference
        this.saveTheme(theme);
        
        // Dispatch custom event for other components
        this.dispatchThemeChange(theme);
        
        console.log('Theme Manager: Theme change complete');
    }
    
    /**
     * Toggle between light and dark themes
     */
    toggleTheme() {
        const currentTheme = this.getCurrentTheme();
        console.log('Theme Manager: Toggling from', currentTheme);
        
        let newTheme;
        
        if (currentTheme === this.THEME_LIGHT) {
            newTheme = this.THEME_DARK;
        } else if (currentTheme === this.THEME_DARK) {
            newTheme = this.THEME_AUTO;
        } else {
            newTheme = this.THEME_LIGHT;
        }
        
        console.log('Theme Manager: Setting new theme to', newTheme);
        this.setTheme(newTheme);
    }
    
    /**
     * Get current theme
     */
    getCurrentTheme() {
        const html = document.documentElement;
        const theme = html.getAttribute('data-theme');
        return theme || this.THEME_LIGHT;
    }
    
    /**
     * Update theme toggle button
     */
    updateToggleButton(theme) {
        // Handle both navbar and floating toggles
        const toggles = document.querySelectorAll('.theme-toggle, .theme-toggle-navbar');
        
        toggles.forEach(toggle => {
            const sunIcon = toggle.querySelector('.sun-icon');
            const moonIcon = toggle.querySelector('.moon-icon');
            const label = toggle.querySelector('.theme-label');
            
            // Update icons
            if (sunIcon && moonIcon) {
                if (theme === this.THEME_DARK) {
                    sunIcon.style.display = 'block';
                    moonIcon.style.display = 'none';
                } else {
                    sunIcon.style.display = 'none';
                    moonIcon.style.display = 'block';
                }
            }
            
            // Update label (only for floating toggle)
            if (label) {
                label.textContent = this.getThemeLabel(theme);
            }
            
            // Update button title
            toggle.title = `Current theme: ${theme}. Click to cycle themes.`;
        });
    }
    
    /**
     * Get human-readable theme label
     */
    getThemeLabel(theme) {
        switch (theme) {
            case this.THEME_DARK:
                return 'Dark';
            case this.THEME_LIGHT:
                return 'Light';
            case this.THEME_AUTO:
                return 'Auto';
            default:
                return 'Light';
        }
    }
    
    /**
     * Add theme toggle button to page
     */
    addThemeToggle() {
        // Don't add if any theme toggle already exists (navbar or floating)
        if (document.querySelector('.theme-toggle') || document.querySelector('.theme-toggle-navbar')) {
            // Update existing buttons instead
            this.updateToggleButton(this.getCurrentTheme());
            return;
        }
        
        const toggle = document.createElement('button');
        toggle.className = 'theme-toggle';
        toggle.setAttribute('aria-label', 'Toggle theme');
        toggle.setAttribute('title', 'Toggle between light, dark, and auto themes');
        
        toggle.innerHTML = `
            <svg class="icon sun-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 17.5C9.5 17.5 7.5 15 7.5 12.5S9.5 7.5 12 7.5 17.5 12.5 15 14.5 12 14.5z"/>
                <path d="M12 2v2c0 .55.45 1 1s1-.45 1-1V3c0-.55-.45-1-1s-.45-1-1-1z"/>
                <path d="M12 7v1c0 .55.45 1 1s1-.45 1-1V7c0-.55-.45-1-1s-.45-1-1-1z"/>
                <path d="M12 12v1c0 .55.45 1 1s1-.45 1-1v-1c0-.55-.45-1-1s-.45-1-1-1z"/>
                <path d="M12 22v1c0 .55.45 1 1s1-.45 1-1v-1c0-.55-.45-1-1s-.45-1-1-1z"/>
            </svg>
            <svg class="icon moon-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M21 12.79A9 9 0 1 1 11.21 12.79 9 9 0 0 0-9-9 9 9 0 0 0 9-9 9 9 0 0 0 9 9z"/>
                <path d="M12.79 21A9 9 0 0 1 1 12.79 21a9 9 0 0 0 9-9 9 9 0 0 0 9-9 9 9 0 0 0 9-9 9 9z"/>
            </svg>
            <span class="theme-label">Light</span>
        `;
        
        // Add click handler
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleTheme();
        });
        
        // Add to page
        document.body.appendChild(toggle);
        
        // Update initial state
        this.updateToggleButton(this.getCurrentTheme());
    }
    
    /**
     * Dispatch theme change event
     */
    dispatchThemeChange(theme) {
        const event = new CustomEvent('themechange', {
            detail: { theme, themeManager: this }
        });
        document.dispatchEvent(event);
    }
    
    /**
     * Get theme CSS variables
     */
    getCSSVariable(variableName) {
        return getComputedStyle(document.documentElement)
            .getPropertyValue(variableName)
            .trim();
    }
    
    /**
     * Check if dark theme is active
     */
    isDarkTheme() {
        const currentTheme = this.getCurrentTheme();
        return currentTheme === this.THEME_DARK || 
               (currentTheme === this.THEME_AUTO && this.getSystemTheme() === this.THEME_DARK);
    }
    
    /**
     * Check if light theme is active
     */
    isLightTheme() {
        const currentTheme = this.getCurrentTheme();
        return currentTheme === this.THEME_LIGHT || 
               (currentTheme === this.THEME_AUTO && this.getSystemTheme() === this.THEME_LIGHT);
    }
}

// Initialize theme manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Theme Manager: Initializing...');
    window.themeManager = new ThemeManager();
    console.log('Theme Manager: Initialized with theme:', window.themeManager.getCurrentTheme());
});

// Fallback initialization if DOMContentLoaded already fired
if (document.readyState === 'loading') {
    // DOM is still loading
    document.addEventListener('DOMContentLoaded', () => {
        console.log('Theme Manager: Initializing (fallback)...');
        window.themeManager = new ThemeManager();
        console.log('Theme Manager: Initialized with theme:', window.themeManager.getCurrentTheme());
    });
} else {
    // DOM is already loaded
    console.log('Theme Manager: Initializing immediately...');
    window.themeManager = new ThemeManager();
    console.log('Theme Manager: Initialized with theme:', window.themeManager.getCurrentTheme());
}

// Export for global access
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
