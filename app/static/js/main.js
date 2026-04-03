/* =============================================
   Portfolio - Main JavaScript
   ============================================= */

// ===== INITIALIZATION ===== //
document.addEventListener('DOMContentLoaded', function() {
    // Load all projects initially
    fetchAndRenderProjects('all');
    initializePortfolio();
});

function initializePortfolio() {
    initializeAOS();
    initializeNavigation();
    initializeSkillBars();
    initializeContactForm();
    initializeFeedbackForm();
    initializeParticles();
    initializeActiveNavigation();
    initializeProjectsSlider();
    initializeSkillsSlider();
    initializeFooter();
    initializeTestimonialsSlider();
    initializeNewsSlider();
}

// ===== SCROLL INDICATOR FUNCTIONALITY ===== //
function scrollToNextSection() {
    // Find the next section after hero
    const heroSection = document.getElementById('hero');
    const sections = document.querySelectorAll('section');
    
    let nextSection = null;
    let foundHero = false;
    
    for (let section of sections) {
        if (foundHero && section.id !== 'hero') {
            nextSection = section;
            break;
        }
        if (section.id === 'hero') {
            foundHero = true;
        }
    }
    
    if (nextSection) {
        const offsetTop = nextSection.offsetTop - 80; // Account for fixed navbar
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

// ===== AOS ANIMATION ===== //
function initializeAOS() {
    AOS.init({
        duration: 1000,
        once: true,
        offset: 100
    });
}

// ===== NAVIGATION ===== //
function initializeNavigation() {
    const navbar = document.getElementById('mainNav');
    if (!navbar) return;

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== SKILL BARS ===== //
function initializeSkillBars() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Make skill cards visible
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                // Animate progress bars
                const progressBar = entry.target.querySelector('.skill-progress-bar');
                if (progressBar) {
                    const width = progressBar.getAttribute('data-width');
                    setTimeout(() => {
                        progressBar.style.width = width;
                    }, 200);
                }
            }
        });
    }, observerOptions);
    
    // Initialize skill cards and start observing
    document.querySelectorAll('.skill-card').forEach(card => {
        // Ensure cards are visible by default
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
}

// ===== CONTACT FORM ===== //
function initializeContactForm() {
    const form = document.querySelector('.contact-form');
    if (!form) return;

    form.addEventListener('submit', handleContactSubmit);
}

function handleContactSubmit(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name')?.value?.trim(),
        email: document.getElementById('email')?.value?.trim(),
        subject: document.getElementById('subject')?.value?.trim(),
        message: document.getElementById('message')?.value?.trim()
    };
    
    // Validation
    if (!validateContactForm(formData)) {
        return;
    }
    
    // Show loading state
    showSubmitLoading();
    
    // Simulate form submission (in production, this would be an API call)
    setTimeout(() => {
        hideSubmitLoading();
        showSuccessMessage();
        resetContactForm();
    }, 2000);
}

function validateContactForm(data) {
    const errors = [];
    
    if (!data.name || data.name.length < 2) {
        errors.push('Please enter a valid name (at least 2 characters)');
    }
    
    if (!data.email || !isValidEmail(data.email)) {
        errors.push('Please enter a valid email address');
    }
    
    if (!data.message || data.message.length < 10) {
        errors.push('Message must be at least 10 characters long');
    }
    
    if (errors.length > 0) {
        showErrors(errors);
        return false;
    }
    
    return true;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showErrors(errors) {
    errors.forEach(error => {
        alert(error);
    });
}

function showSubmitLoading() {
    const submitBtn = document.querySelector('.btn-submit');
    if (submitBtn) {
        submitBtn.innerHTML = '<div class="loading-spinner"></div> Sending...';
        submitBtn.disabled = true;
    }
}

function hideSubmitLoading() {
    const submitBtn = document.querySelector('.btn-submit');
    if (submitBtn) {
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
        submitBtn.disabled = false;
    }
}

function showSuccessMessage() {
    // In production, this would show a success message
    alert('Message sent successfully! We\'ll get back to you soon.');
}

function resetContactForm() {
    const form = document.querySelector('.contact-form');
    if (form) {
        form.reset();
    }
}

// ===== PARTICLES ===== //
function initializeParticles() {
    setInterval(createParticle, 2000);
}

function createParticle() {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 20 + 's';
    particle.style.animationDuration = (15 + Math.random() * 10) + 's';
    
    const heroParticles = document.querySelector('.hero-particles');
    heroParticles?.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        particle.remove();
    }, 25000);
}

// ===== ACTIVE NAVIGATION ===== //
function initializeActiveNavigation() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').slice(1) === current) {
                link.classList.add('active');
            }
        });
    });
}

// ===== UTILITIES ===== //
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== PROJECTS SLIDER FUNCTIONALITY ===== //
let currentProjectSlide = 0;
let totalProjectSlides = 0;
let projectsPerView = 3;
let isProjectAnimating = false;
let autoSlideInterval;

function initializeProjectsSlider() {
    const track = document.getElementById('projectsSliderTrack');
    const slides = document.querySelectorAll('.project-slide-item');
    
    if (!track || !slides.length) return;
    
    totalProjectSlides = slides.length;
    updateProjectsPerView();
    updateProjectSliderControls();
    startAutoSlide();
    
    // Add touch/swipe support
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    
    track.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        isDragging = true;
        track.style.cursor = 'grabbing';
        stopAutoSlide();
    }, { passive: true });
    
    track.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        currentX = e.touches[0].clientX;
    }, { passive: true });
    
    track.addEventListener('touchend', () => {
        if (!isDragging) return;
        isDragging = false;
        track.style.cursor = 'grab';
        
        const diff = startX - currentX;
        if (Math.abs(diff) > 50) {
            if (diff > 0) {
                navigateProjects('next');
            } else {
                navigateProjects('prev');
            }
        } else {
            startAutoSlide();
        }
    });
    
    // Pause on hover
    const wrapper = document.querySelector('.projects-slider-wrapper');
    if (wrapper) {
        wrapper.addEventListener('mouseenter', stopAutoSlide);
        wrapper.addEventListener('mouseleave', startAutoSlide);
    }
    
    // Update on window resize
    window.addEventListener('resize', debounce(() => {
        updateProjectsPerView();
        updateProjectSliderControls();
        goToProjectSlide(currentProjectSlide, false);
    }, 250));
}

function updateProjectsPerView() {
    const width = window.innerWidth;
    if (width >= 992) {
        projectsPerView = 3;
    } else if (width >= 768) {
        projectsPerView = 2;
    } else {
        projectsPerView = 1;
    }
}

function navigateProjects(direction) {
    if (isProjectAnimating) return;
    
    const maxSlide = Math.max(0, totalProjectSlides - projectsPerView);
    
    if (direction === 'next') {
        currentProjectSlide = Math.min(currentProjectSlide + 1, maxSlide);
    } else {
        currentProjectSlide = Math.max(currentProjectSlide - 1, 0);
    }
    
    goToProjectSlide(currentProjectSlide, true);
    resetAutoSlide();
}

function goToProjectSlide(slideIndex, animate = true) {
    if (isProjectAnimating && animate) return;
    
    const track = document.getElementById('projectsSliderTrack');
    if (!track) return;
    
    const maxSlide = Math.max(0, totalProjectSlides - projectsPerView);
    currentProjectSlide = Math.min(Math.max(0, slideIndex), maxSlide);
    
    const slideWidth = track.querySelector('.project-slide-item')?.offsetWidth || 0;
    const gap = 32; // CSS gap
    const offset = currentProjectSlide * (slideWidth + gap);
    
    if (animate) {
        isProjectAnimating = true;
        track.style.transform = `translateX(-${offset}px)`;
        
        setTimeout(() => {
            isProjectAnimating = false;
        }, 600);
    } else {
        track.style.transform = `translateX(-${offset}px)`;
    }
    
    updateProjectSliderControls();
}

function updateProjectSliderControls() {
    const prevBtn = document.querySelector('.slider-nav-prev');
    const nextBtn = document.querySelector('.slider-nav-next');
    const dots = document.querySelectorAll('.slider-dot');
    
    if (!prevBtn || !nextBtn) return;
    
    const maxSlide = Math.max(0, totalProjectSlides - projectsPerView);
    
    // Update button states
    prevBtn.classList.toggle('disabled', currentProjectSlide === 0);
    nextBtn.classList.toggle('disabled', currentProjectSlide >= maxSlide);
    
    // Update dots (show dots for each possible slide position)
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentProjectSlide);
    });
}

function startAutoSlide() {
    stopAutoSlide();
    autoSlideInterval = setInterval(() => {
        const maxSlide = Math.max(0, totalProjectSlides - projectsPerView);
        if (currentProjectSlide >= maxSlide) {
            currentProjectSlide = 0;
        } else {
            currentProjectSlide++;
        }
        goToProjectSlide(currentProjectSlide, true);
    }, 5000);
}

function stopAutoSlide() {
    if (autoSlideInterval) {
        clearInterval(autoSlideInterval);
        autoSlideInterval = null;
    }
}

function resetAutoSlide() {
    stopAutoSlide();
    startAutoSlide();
}

// ===== SKILLS SLIDER FUNCTIONALITY ===== //
let currentSkillSlide = 0;
let totalSkillSlides = 0;
let skillsPerView = 4;
let isSkillAnimating = false;
let autoSkillSlideInterval;

function initializeSkillsSlider() {
    const track = document.getElementById('skillsSliderTrack');
    const slides = document.querySelectorAll('.skill-slide-item');
    
    if (!track || !slides.length) return;
    
    totalSkillSlides = slides.length;
    updateSkillsPerView();
    updateSkillSliderControls();
    startAutoSkillSlide();
    
    // Add touch/swipe support
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    
    track.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        isDragging = true;
        track.style.cursor = 'grabbing';
        stopAutoSkillSlide();
    }, { passive: true });
    
    track.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        currentX = e.touches[0].clientX;
    }, { passive: true });
    
    track.addEventListener('touchend', () => {
        if (!isDragging) return;
        isDragging = false;
        track.style.cursor = 'grab';
        
        const diff = startX - currentX;
        if (Math.abs(diff) > 50) {
            if (diff > 0) {
                navigateSkills('next');
            } else {
                navigateSkills('prev');
            }
        } else {
            startAutoSkillSlide();
        }
    });
    
    // Pause on hover
    const wrapper = document.querySelector('#skills .projects-slider-wrapper');
    if (wrapper) {
        wrapper.addEventListener('mouseenter', stopAutoSkillSlide);
        wrapper.addEventListener('mouseleave', startAutoSkillSlide);
    }
    
    // Update on window resize
    window.addEventListener('resize', debounce(() => {
        updateSkillsPerView();
        updateSkillSliderControls();
        goToSkillSlide(currentSkillSlide, false);
    }, 250));
}

function updateSkillsPerView() {
    const width = window.innerWidth;
    if (width >= 1200) {
        skillsPerView = 4;
    } else if (width >= 992) {
        skillsPerView = 3;
    } else if (width >= 768) {
        skillsPerView = 2;
    } else {
        skillsPerView = 1;
    }
}

function navigateSkills(direction) {
    if (isSkillAnimating) return;
    
    const maxSlide = Math.max(0, totalSkillSlides - skillsPerView);
    
    if (direction === 'next') {
        currentSkillSlide = Math.min(currentSkillSlide + 1, maxSlide);
    } else {
        currentSkillSlide = Math.max(currentSkillSlide - 1, 0);
    }
    
    goToSkillSlide(currentSkillSlide, true);
    resetAutoSkillSlide();
}

function goToSkillSlide(slideIndex, animate = true) {
    if (isSkillAnimating && animate) return;
    
    const track = document.getElementById('skillsSliderTrack');
    if (!track) return;
    
    const maxSlide = Math.max(0, totalSkillSlides - skillsPerView);
    currentSkillSlide = Math.min(Math.max(0, slideIndex), maxSlide);
    
    const slideWidth = track.querySelector('.skill-slide-item')?.offsetWidth || 0;
    const gap = 32; // CSS gap
    const offset = currentSkillSlide * (slideWidth + gap);
    
    if (animate) {
        isSkillAnimating = true;
        track.style.transform = `translateX(-${offset}px)`;
        
        setTimeout(() => {
            isSkillAnimating = false;
        }, 600);
    } else {
        track.style.transform = `translateX(-${offset}px)`;
    }
    
    updateSkillSliderControls();
}

function updateSkillSliderControls() {
    const prevBtn = document.querySelector('#skills .slider-nav-prev');
    const nextBtn = document.querySelector('#skills .slider-nav-next');
    const dots = document.querySelectorAll('#skillsSliderDots .slider-dot');
    
    if (!prevBtn || !nextBtn) return;
    
    const maxSlide = Math.max(0, totalSkillSlides - skillsPerView);
    
    // Update button states
    prevBtn.classList.toggle('disabled', currentSkillSlide === 0);
    nextBtn.classList.toggle('disabled', currentSkillSlide >= maxSlide);
    
    // Update dots
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSkillSlide);
    });
}

function startAutoSkillSlide() {
    stopAutoSkillSlide();
    autoSkillSlideInterval = setInterval(() => {
        const maxSlide = Math.max(0, totalSkillSlides - skillsPerView);
        if (currentSkillSlide >= maxSlide) {
            currentSkillSlide = 0;
        } else {
            currentSkillSlide++;
        }
        goToSkillSlide(currentSkillSlide, true);
    }, 4000);
}

function stopAutoSkillSlide() {
    if (autoSkillSlideInterval) {
        clearInterval(autoSkillSlideInterval);
        autoSkillSlideInterval = null;
    }
}

function resetAutoSkillSlide() {
    stopAutoSkillSlide();
    startAutoSkillSlide();
}

// ===== FOOTER FUNCTIONALITY ===== //
function initializeFooter() {
    // Newsletter Form
    const newsletterForm = document.getElementById('newsletterForm');
    const newsletterSuccess = document.getElementById('newsletterSuccess');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = this.querySelector('.newsletter-input').value;
            
            // Simulate newsletter subscription
            if (email) {
                // Show success message
                newsletterSuccess.classList.add('show');
                
                // Reset form
                this.reset();
                
                // Hide success message after 5 seconds
                setTimeout(() => {
                    newsletterSuccess.classList.remove('show');
                }, 5000);
                
                // Here you would normally send the email to your server
                console.log('Newsletter subscription:', email);
            }
        });
    }
    
    // Back to Top Button
    const backToTopBtn = document.getElementById('backToTop');
    
    if (backToTopBtn) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        
        // Scroll to top when clicked
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Smooth scroll for footer links
    const footerLinks = document.querySelectorAll('.footer-link[href^="#"]');
    footerLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== ENHANCED CONTACT FORM FUNCTIONALITY ===== //
function initializeContactForm() {
    const contactForm = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');
    const resetBtn = document.getElementById('resetBtn');
    const formLoading = document.getElementById('formLoading');
    const messageTextarea = document.getElementById('message');
    const charCount = document.getElementById('charCount');
    
    if (!contactForm) return;
    
    // Character counter for message
    if (messageTextarea && charCount) {
        messageTextarea.addEventListener('input', function() {
            const length = this.value.length;
            const maxLength = 500;
            charCount.textContent = length;
            
            if (length > maxLength) {
                this.value = this.value.substring(0, maxLength);
                charCount.textContent = maxLength;
            }
            
            // Change color based on character count
            if (length > 400) {
                charCount.style.color = '#e53e3e';
            } else if (length > 300) {
                charCount.style.color = '#ed8936';
            } else {
                charCount.style.color = '#a0aec0';
            }
        });
    }
    
    // Form validation
    function validateForm() {
        let isValid = true;
        const requiredFields = contactForm.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            const feedback = field.parentElement.querySelector('.form-feedback');
            
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                if (feedback) {
                    feedback.textContent = 'This field is required';
                    feedback.style.color = '#e53e3e';
                }
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
                if (feedback) {
                    feedback.textContent = '';
                }
                
                // Email validation
                if (field.type === 'email') {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(field.value)) {
                        field.classList.add('is-invalid');
                        if (feedback) {
                            feedback.textContent = 'Please enter a valid email address';
                            feedback.style.color = '#e53e3e';
                        }
                        isValid = false;
                    }
                }
                
                // Phone validation (optional)
                if (field.type === 'tel' && field.value) {
                    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
                    if (!phoneRegex.test(field.value)) {
                        field.classList.add('is-invalid');
                        if (feedback) {
                            feedback.textContent = 'Please enter a valid phone number';
                            feedback.style.color = '#e53e3e';
                        }
                        isValid = false;
                    }
                }
            }
        });
        
        return isValid;
    }
    
    // Real-time validation
    const formInputs = contactForm.querySelectorAll('.form-control, .form-select');
    formInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const feedback = this.parentElement.querySelector('.form-feedback');
            
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('is-invalid');
                if (feedback) {
                    feedback.textContent = 'This field is required';
                    feedback.style.color = '#e53e3e';
                }
            } else {
                this.classList.remove('is-invalid');
                if (feedback) {
                    feedback.textContent = '';
                }
                
                // Email validation
                if (this.type === 'email' && this.value) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(this.value)) {
                        this.classList.add('is-invalid');
                        if (feedback) {
                            feedback.textContent = 'Please enter a valid email address';
                            feedback.style.color = '#e53e3e';
                        }
                    }
                }
            }
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                this.classList.remove('is-invalid');
                const feedback = this.parentElement.querySelector('.form-feedback');
                if (feedback) {
                    feedback.textContent = '';
                }
            }
        });
    });
    
    // Form submission
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (!validateForm()) {
                // Shake animation for invalid form
                contactForm.style.animation = 'shake 0.5s';
                setTimeout(() => {
                    contactForm.style.animation = '';
                }, 500);
                return;
            }
            
            // Show loading state
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Sending...</span>';
            }
            
            if (formLoading) {
                formLoading.style.display = 'block';
            }
            
            // Simulate form submission
            setTimeout(() => {
                // Hide loading state
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-check"></i> <span>Message Sent!</span>';
                    submitBtn.style.background = 'linear-gradient(135deg, #48bb78, #38a169)';
                }
                
                if (formLoading) {
                    formLoading.style.display = 'none';
                }
                
                // Reset form after 3 seconds
                setTimeout(() => {
                    contactForm.reset();
                    if (submitBtn) {
                        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> <span>Send Message</span>';
                        submitBtn.style.background = '';
                    }
                    if (charCount) {
                        charCount.textContent = '0';
                        charCount.style.color = '#a0aec0';
                    }
                }, 3000);
                
                // Actually submit the form to the server
                const formData = new FormData(contactForm);
                
                // Submit form using fetch
                fetch('/contact', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (response.redirected) {
                        // If server redirects, follow the redirect
                        window.location.href = response.url;
                    } else {
                        // Otherwise, show success and reset form
                        showSuccessMessage();
                        setTimeout(() => {
                            contactForm.reset();
                            if (submitBtn) {
                                submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> <span>Send Message</span>';
                                submitBtn.style.background = '';
                            }
                            if (charCount) {
                                charCount.textContent = '0';
                                charCount.style.color = '#a0aec0';
                            }
                        }, 3000);
                    }
                })
                .catch(error => {
                    console.error('Error submitting form:', error);
                    // Show error message
                    if (submitBtn) {
                        submitBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> <span>Error!</span>';
                        submitBtn.style.background = 'linear-gradient(135deg, #e53e3e, #c53030)';
                    }
                    setTimeout(() => {
                        if (submitBtn) {
                            submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> <span>Send Message</span>';
                            submitBtn.style.background = '';
                        }
                    }, 2000);
                });
                
            }, 2000);
        });
    }
    
    // Reset button functionality
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            contactForm.reset();
            
            // Clear all validation states
            formInputs.forEach(input => {
                input.classList.remove('is-invalid');
                const feedback = input.parentElement.querySelector('.form-feedback');
                if (feedback) {
                    feedback.textContent = '';
                }
            });
            
            // Reset character counter
            if (charCount) {
                charCount.textContent = '0';
                charCount.style.color = '#a0aec0';
            }
            
            // Add animation
            contactForm.style.animation = 'fadeIn 0.5s';
            setTimeout(() => {
                contactForm.style.animation = '';
            }, 500);
        });
    }
    
    // Add shake animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
            20%, 40%, 60%, 80% { transform: translateX(10px); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .form-control.is-invalid {
            border-color: #e53e3e !important;
            box-shadow: 0 0 0 3px rgba(229, 62, 62, 0.1) !important;
        }
        
        .form-control.is-valid {
            border-color: #48bb78 !important;
            box-shadow: 0 0 0 3px rgba(72, 187, 120, 0.1) !important;
        }
    `;
    document.head.appendChild(style);
}

// ===== SWIPER TESTIMONIALS SLIDER ===== //
function initializeTestimonialsSlider() {
    const swiper = new Swiper('.testimonialSwiper', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
            dynamicBullets: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 1,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 2,
                spaceBetween: 30,
            },
            1024: {
                slidesPerView: 2,
                spaceBetween: 40,
            },
            1200: {
                slidesPerView: 3,
                spaceBetween: 40,
            },
        },
        effect: 'slide',
        speed: 800,
        grabCursor: true,
        simulateTouch: true,
        touchRatio: 1,
        touchAngle: 45,
        longSwipes: true,
        longSwipesRatio: 0.5,
        shortSwipes: true,
        allowTouchMove: true,
        resistance: true,
        resistanceRatio: 0.85,
        watchSlidesProgress: true,
        watchSlidesVisibility: true,
        centeredSlides: false,
        slideToClickedSlide: false,
        preventClicks: true,
        preventClicksPropagation: true,
        noSwiping: false,
        noSwipingClass: 'swiper-no-swiping',
        passiveListeners: true,
        containerModifierClass: 'swiper-',
        slideClass: 'swiper-slide',
        slideBlankClass: 'swiper-slide-blank',
        slideActiveClass: 'swiper-slide-active',
        slideDuplicateActiveClass: 'swiper-slide-duplicate-active',
        slideVisibleClass: 'swiper-slide-visible',
        slideDuplicateClass: 'swiper-slide-duplicate',
        slideNextClass: 'swiper-slide-next',
        slideDuplicateNextClass: 'swiper-slide-duplicate-next',
        slidePrevClass: 'swiper-slide-prev',
        slideDuplicatePrevClass: 'swiper-slide-duplicate-prev',
        wrapperClass: 'swiper-wrapper',
        runCallbacksOnInit: true,
    });
    
    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            swiper.slidePrev();
        } else if (e.key === 'ArrowRight') {
            swiper.slideNext();
        }
    });
    
    // Pause on hover
    const swiperContainer = document.querySelector('.testimonialSwiper');
    if (swiperContainer) {
        swiperContainer.addEventListener('mouseenter', () => {
            swiper.autoplay.stop();
        });
        
        swiperContainer.addEventListener('mouseleave', () => {
            swiper.autoplay.start();
        });
    }
}

// ===== RECENT PROJECTS NEWS SLIDER ===== //
let newsRefreshInterval;

function initializeNewsSlider() {
    const newsTrack = document.getElementById('newsSliderTrack');
    if (!newsTrack) return;
    
    // Fetch projects immediately
    fetchRecentProjects();
    
    // Auto-refresh every 60 seconds
    newsRefreshInterval = setInterval(fetchRecentProjects, 60000);
    
    // Handle visibility change to pause/resume
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            clearInterval(newsRefreshInterval);
        } else {
            fetchRecentProjects();
            newsRefreshInterval = setInterval(fetchRecentProjects, 60000);
        }
    });
}

async function fetchRecentProjects() {
    const newsTrack = document.getElementById('newsSliderTrack');
    if (!newsTrack) return;
    
    try {
        const response = await fetch('/recent-projects');
        const data = await response.json();
        
        if (data.success && data.projects && data.projects.length > 0) {
            renderNewsItems(data.projects);
        } else {
            // Show fallback message if no projects
            newsTrack.innerHTML = `
                <div class="news-item" style="justify-content: center; opacity: 0.6;">
                    <div class="news-item-content" style="text-align: center;">
                        <p class="news-item-desc">No recent projects yet. Check back soon!</p>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error fetching recent projects:', error);
        // Don't clear existing content on error, just log it
    }
}

function renderNewsItems(projects) {
    const newsTrack = document.getElementById('newsSliderTrack');
    if (!newsTrack) return;
    
    // Create HTML for projects (duplicate for infinite scroll)
    const createNewsItem = (project) => {
        const imageUrl = project.image 
            ? `/static/uploads/${project.image}` 
            : 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=100&h=100&fit=crop';
        
        const projectUrl = project.live_link || project.github_link || '#projects';
        
        return `
            <div class="news-item" onclick="window.open('${projectUrl}', '_blank')">
                <img src="${imageUrl}" alt="${project.title}" class="news-item-image" loading="lazy">
                <div class="news-item-content">
                    <h5 class="news-item-title">${escapeHtml(project.title)}</h5>
                    <p class="news-item-desc">${escapeHtml(project.description)}</p>
                    <span class="news-item-date">
                        <i class="fas fa-clock"></i>
                        ${project.created_at || 'Recently'}
                    </span>
                </div>
            </div>
        `;
    };
    
    // Generate content - duplicate for seamless infinite scroll
    const projectsHtml = projects.map(createNewsItem).join('');
    const duplicatedHtml = projectsHtml + projectsHtml; // Duplicate for infinite loop
    
    newsTrack.innerHTML = duplicatedHtml;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== PROJECT FILTERING ===== //
function filterProjects(category) {
    // Update active tab
    const tabs = document.querySelectorAll('.project-tab');
    tabs.forEach(tab => {
        if (tab.dataset.category === category) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
    
    // Filter project cards on the page
    const projectCards = document.querySelectorAll('.project-card');
    const projectsGrid = document.getElementById('projectsGrid');
    
    // Add loading state
    projectsGrid.classList.add('loading');
    
    projectCards.forEach((card, index) => {
        const cardCategory = card.dataset.category || 'web_dev';
        
        if (category === 'all' || cardCategory === category) {
            // Show card with animation
            card.classList.remove('hiding');
            card.classList.add('showing');
            card.style.display = '';
            
            // Stagger animation
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
            }, index * 100);
        } else {
            // Hide card with animation
            card.classList.remove('showing');
            card.classList.add('hiding');
            card.style.opacity = '0';
            card.style.transform = 'scale(0.8)';
            
            setTimeout(() => {
                card.style.display = 'none';
            }, 300);
        }
    });
    
    // Remove loading state
    setTimeout(() => {
        projectsGrid.classList.remove('loading');
    }, 400);
    
    // Check if any projects are visible
    const visibleCards = Array.from(projectCards).filter(card => 
        card.style.display !== 'none'
    );
    
    // Show empty state if no projects
    if (visibleCards.length === 0) {
        showEmptyState(category);
    } else {
        hideEmptyState();
    }
}

// ===== EMPTY STATE FUNCTIONS ===== //
function showEmptyState(category) {
    const projectsGrid = document.getElementById('projectsGrid');
    if (!projectsGrid) return;
    
    const emptyState = document.createElement('div');
    emptyState.className = 'projects-grid-empty';
    emptyState.innerHTML = `
        <i class="fas fa-folder-open"></i>
        <h3>No ${getCategoryName(category)} Projects</h3>
        <p>Check back soon for new ${getCategoryName(category).toLowerCase()} projects!</p>
    `;
    
    projectsGrid.appendChild(emptyState);
}

function hideEmptyState() {
    const emptyState = document.querySelector('.projects-grid-empty');
    if (emptyState) {
        emptyState.remove();
    }
}

function getCategoryName(category) {
    const names = {
        'all': 'Projects',
        'web_dev': 'Web Development',
        'graphic_design': 'Graphic Design',
        'video_editing': 'Video Editing'
    };
    return names[category] || 'Projects';
}

// ===== FETCH AND RENDER PROJECTS ===== //
async function fetchAndRenderProjects(category) {
    const projectsGrid = document.getElementById('projectsGrid');
    if (!projectsGrid) return;
    
    // If grid already has content from server, don't fetch
    if (projectsGrid.children.length > 0) return;
    
    try {
        const response = await fetch(`/api/projects?category=${category}&limit=12`);
        const data = await response.json();
        
        if (data.success && data.projects.length > 0) {
            renderProjectsToGrid(data.projects, projectsGrid);
        }
    } catch (error) {
        console.error('Error fetching projects:', error);
    }
}

function renderProjectsToGrid(projects, grid) {
    if (!grid || projects.length === 0) return;
    
    const projectsHtml = projects.map(project => {
        const categoryBadge = getCategoryBadge(project.category);
        const linkButton = getProjectLinkButton(project);
        const techTags = project.technologies ? project.technologies.split(',').slice(0, 4).map(tech => 
            `<span class="tech-tag">${tech.trim()}</span>`
        ).join('') : '';
        
        return `
        <div class="col-lg-4 col-md-6 project-item" data-category="${project.category || 'web_dev'}" data-aos="fade-up">
            <div class="project-card">
                <div class="project-image">
                    ${project.image ? 
                        `<img src="/static/uploads/${project.image}" alt="${escapeHtml(project.title)}">` :
                        `<img src="https://images.unsplash.com/photo-1460925895917-4365d14bab8c?w=400&h=250&fit=crop&crop=entropy&auto=format" alt="${escapeHtml(project.title)}">`
                    }
                    <div class="project-overlay"></div>
                    <div class="project-category-badge">
                        ${categoryBadge}
                    </div>
                </div>
                <div class="project-content">
                    <h3 class="project-title">${escapeHtml(project.title)}</h3>
                    <p class="project-description">
                        ${project.short_description || 'No description available.'}
                    </p>
                    
                    ${techTags ? `<div class="project-tech">${techTags}</div>` : ''}
                    
                    <div class="project-links">
                        ${linkButton}
                    </div>
                </div>
            </div>
        </div>`;
    }).join('');
    
    if (projects.length > 0) {
        grid.innerHTML = projectsHtml;
        if (typeof AOS !== 'undefined') {
            AOS.refresh();
        }
    }
}

function getCategoryBadge(category) {
    switch(category) {
        case 'web_dev':
            return '<i class="fas fa-code"></i> Web Dev';
        case 'graphic_design':
            return '<i class="fas fa-palette"></i> Design';
        case 'video_editing':
            return '<i class="fas fa-video"></i> Video';
        default:
            return '<i class="fas fa-code"></i> Web Dev';
    }
}

function getProjectLinkButton(project) {
    let buttons = '';
    
    if (project.github_link && project.category === 'web_dev') {
        buttons += `<a href="${project.github_link}" class="project-link project-link-secondary" target="_blank">
            <i class="fab fa-github"></i> Code
        </a>`;
    }
    
    if (project.live_link) {
        let icon = 'fa-external-link-alt';
        let text = 'Live Demo';
        
        if (project.category === 'video_editing') {
            icon = 'fa-play';
            text = 'Watch';
        } else if (project.category === 'graphic_design') {
            icon = 'fa-eye';
            text = 'View';
        }
        
        buttons += `<a href="${project.live_link}" class="project-link project-link-primary" target="_blank">
            <i class="fas ${icon}"></i> ${text}
        </a>`;
    }
    
    return buttons;
}

// ===== FLOATING NOTIFICATION SYSTEM ===== //
function showFloatingNotification(message, type = 'success') {
    // Remove any existing notifications
    const existing = document.querySelector('.floating-notification');
    if (existing) {
        existing.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `floating-notification floating-notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Add to page
    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.classList.add('notification-hiding');
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// ===== FEEDBACK FORM AJAX SUBMISSION ===== //
function initializeFeedbackForm() {
    const feedbackForm = document.getElementById('feedbackForm');
    if (!feedbackForm) return;

    feedbackForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Show loading state
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
        submitBtn.disabled = true;

        // Submit via AJAX
        fetch('/feedback', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success notification
                showFloatingNotification('Feedback submitted successfully! Thank you for your feedback.', 'success');
                
                // Reset form
                feedbackForm.reset();
                
                // Scroll to feedback section
                setTimeout(() => {
                    document.getElementById('feedback').scrollIntoView({ 
                        behavior: 'smooth',
                        block: 'start'
                    });
                }, 500);
                
            } else {
                // Show error notification
                showFloatingNotification(data.message || 'Error submitting feedback. Please try again.', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showFloatingNotification('Error submitting feedback. Please try again.', 'error');
        })
        .finally(() => {
            // Reset button
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
    });
}
