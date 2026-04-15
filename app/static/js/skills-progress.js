// Dynamic Skills Progress Bar Animation
document.addEventListener('DOMContentLoaded', function() {
    // Function to animate progress bars with actual database values
    function animateProgressBars() {
        const progressBars = document.querySelectorAll('.skill-progress-bar');
        
        progressBars.forEach((bar, index) => {
            const targetWidth = bar.getAttribute('data-width');
            const percentageLabel = bar.parentElement.querySelector('.skill-progress-label');
            
            if (targetWidth && percentageLabel) {
                // Extract numeric value from percentage (e.g., "85%" -> 85)
                const numericValue = parseInt(targetWidth.replace('%', ''));
                
                // Set initial state
                bar.style.width = '0%';
                
                // Animate after a delay for staggered effect
                setTimeout(() => {
                    // Animate the progress bar
                    bar.style.transition = 'width 2.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                    bar.style.width = targetWidth;
                    
                    // Animate the percentage label
                    animatePercentage(percentageLabel, numericValue);
                }, 200 + (index * 100)); // Staggered animation
            }
        });
    }
    
    // Function to animate percentage counting
    function animatePercentage(element, targetValue) {
        let currentValue = 0;
        const increment = targetValue / 50; // Divide animation into 50 steps
        const duration = 2500; // 2.5 seconds
        const stepTime = duration / 50;
        
        const timer = setInterval(() => {
            currentValue += increment;
            
            if (currentValue >= targetValue) {
                currentValue = targetValue;
                clearInterval(timer);
            }
            
            // Update the label content
            element.textContent = Math.round(currentValue);
        }, stepTime);
    }
    
    // Intersection Observer for triggering animation when in viewport
    function setupIntersectionObserver() {
        const skillsSection = document.querySelector('.skills-section');
        
        if (skillsSection) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateProgressBars();
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.3, // Trigger when 30% of section is visible
                rootMargin: '0px 0px -100px 0px'
            });
            
            observer.observe(skillsSection);
        }
    }
    
    // Initialize animations
    setupIntersectionObserver();
    
    // Fallback for immediate animation if intersection observer doesn't work
    setTimeout(() => {
        const progressBars = document.querySelectorAll('.skill-progress-bar');
        let hasAnimated = false;
        
        progressBars.forEach(bar => {
            if (bar.style.width !== '0%') {
                hasAnimated = true;
            }
        });
        
        if (!hasAnimated) {
            animateProgressBars();
        }
    }, 1000);
});

// Handle theme changes to ensure progress bars remain visible
document.addEventListener('themeChanged', function() {
    const progressBars = document.querySelectorAll('.skill-progress-bar');
    progressBars.forEach(bar => {
        // Ensure colors remain visible on theme change
        const currentWidth = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = currentWidth;
        }, 100);
    });
});
