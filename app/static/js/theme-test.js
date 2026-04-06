/**
 * Theme System Test Script
 * Run this in the browser console to test the theme system
 */

function testThemeSystem() {
    console.log('🧪 Testing Theme System...');
    
    // Test 1: Check if theme manager exists
    if (!window.themeManager) {
        console.error('❌ Theme Manager not found!');
        return false;
    }
    console.log('✅ Theme Manager exists');
    
    // Test 2: Check current theme
    const currentTheme = window.themeManager.getCurrentTheme();
    console.log('✅ Current theme:', currentTheme);
    
    // Test 3: Check if CSS variables are working
    const html = document.documentElement;
    const bgColor = getComputedStyle(html).getPropertyValue('--bg-primary').trim();
    const textColor = getComputedStyle(html).getPropertyValue('--text-primary').trim();
    
    console.log('✅ CSS Variables:');
    console.log('   --bg-primary:', bgColor);
    console.log('   --text-primary:', textColor);
    
    // Test 4: Check data-theme attribute
    const dataTheme = html.getAttribute('data-theme');
    console.log('✅ data-theme attribute:', dataTheme || 'null (light mode)');
    
    // Test 5: Test theme toggle
    console.log('🔄 Testing theme toggle...');
    const originalTheme = window.themeManager.getCurrentTheme();
    
    try {
        window.themeManager.toggleTheme();
        const newTheme = window.themeManager.getCurrentTheme();
        console.log('✅ Theme toggled from', originalTheme, 'to', newTheme);
        
        // Test 6: Check if visual changes occurred
        const newBgColor = getComputedStyle(html).getPropertyValue('--bg-primary').trim();
        const newTextColor = getComputedStyle(html).getPropertyValue('--text-primary').trim();
        
        if (newBgColor !== bgColor || newTextColor !== textColor) {
            console.log('✅ Visual theme changes detected');
        } else {
            console.warn('⚠️ No visual changes detected - CSS variables may not be applied');
        }
        
        // Test 7: Check toggle buttons
        const toggles = document.querySelectorAll('.theme-toggle, .theme-toggle-navbar');
        console.log('✅ Found', toggles.length, 'theme toggle buttons');
        
        toggles.forEach((toggle, index) => {
            const sunIcon = toggle.querySelector('.sun-icon');
            const moonIcon = toggle.querySelector('.moon-icon');
            
            if (sunIcon && moonIcon) {
                const sunDisplay = getComputedStyle(sunIcon).display;
                const moonDisplay = getComputedStyle(moonIcon).display;
                
                console.log(`✅ Toggle ${index + 1}: Sun icon display:`, sunDisplay, 'Moon icon display:', moonDisplay);
            } else {
                console.warn(`⚠️ Toggle ${index + 1}: Missing icons`);
            }
        });
        
        // Test 8: Test localStorage
        const savedTheme = localStorage.getItem('portfolio-theme');
        console.log('✅ Saved theme in localStorage:', savedTheme);
        
        console.log('🎉 Theme system test complete!');
        return true;
        
    } catch (error) {
        console.error('❌ Error during theme toggle test:', error);
        return false;
    }
}

// Test individual themes
function testIndividualThemes() {
    console.log('🧪 Testing Individual Themes...');
    
    const themes = ['light', 'dark', 'auto'];
    
    themes.forEach(theme => {
        console.log(`🔄 Testing ${theme} theme...`);
        
        window.themeManager.setTheme(theme);
        const currentTheme = window.themeManager.getCurrentTheme();
        
        const bgColor = getComputedStyle(document.documentElement).getPropertyValue('--bg-primary').trim();
        const textColor = getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim();
        
        console.log(`✅ ${theme} theme applied:`);
        console.log(`   Current theme: ${currentTheme}`);
        console.log(`   Background: ${bgColor}`);
        console.log(`   Text: ${textColor}`);
        console.log(`   data-theme: ${document.documentElement.getAttribute('data-theme') || 'null'}`);
        
        // Wait a moment for visual changes
        setTimeout(() => {
            console.log(`   ✨ ${theme} theme should be visible now`);
        }, 100);
    });
}

// Manual theme setter for testing
function setThemeManually(theme) {
    const html = document.documentElement;
    
    // Remove existing theme
    html.removeAttribute('data-theme');
    
    // Set new theme
    if (theme !== 'light') {
        html.setAttribute('data-theme', theme);
    }
    
    // Update toggle buttons
    const toggles = document.querySelectorAll('.theme-toggle, .theme-toggle-navbar');
    toggles.forEach(toggle => {
        const sunIcon = toggle.querySelector('.sun-icon');
        const moonIcon = toggle.querySelector('.moon-icon');
        
        if (sunIcon && moonIcon) {
            if (theme === 'dark') {
                sunIcon.style.display = 'block';
                moonIcon.style.display = 'none';
            } else {
                sunIcon.style.display = 'none';
                moonIcon.style.display = 'block';
            }
        }
    });
    
    console.log(`✅ Manually set theme to: ${theme}`);
    return theme;
}

// Export functions for global access
window.testThemeSystem = testThemeSystem;
window.testIndividualThemes = testIndividualThemes;
window.setThemeManually = setThemeManually;

console.log('🧪 Theme test functions loaded!');
console.log('Run testThemeSystem() to test the theme system');
console.log('Run testIndividualThemes() to test each theme');
console.log('Run setThemeManually("dark") to manually set a theme');
