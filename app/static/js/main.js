/* =============================================
   ELITE PORTFOLIO - MAIN JAVASCRIPT v4.0
   Professional, Optimized, Feature-Rich
   ============================================= */

// ============================================
// GLOBAL VARIABLES & CONFIGURATION
// ============================================

const AppConfig = {
    // Scroll settings
    scrollOffset: 80,
    scrollThreshold: 50,
    
    // Animation settings
    aosDuration: 1000,
    aosOffset: 100,
    
    // Slider settings
    autoSlideDelay: 5000,
    skillSlideDelay: 4000,
    newsRefreshInterval: 300000, // 5 minutes
    
    // Form settings
    maxMessageLength: 500,
    notificationDuration: 5000,
    
    // Breakpoints
    breakpoints: {
        mobile: 768,
        tablet: 992,
        desktop: 1200
    }
};

// ============================================
// CORE INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Core features
    initializeAOS();
    initializeNavigation();
    initializeActiveNavigation();
    initializeScrollIndicators();
    
    // Content features
    initializeProjects();
    initializeSkillsSlider();
    initializeTestimonialsSlider();
    initializeNewsSlider();
    
    // Form features
    initializeContactForm();
    initializeFeedbackForm();
    
    // UI features
    initializeParticles();
    initializeFooter();
    initializeBackToTop();
    
    // Performance optimizations
    initializeLazyLoading();
    initializeResizeHandler();
    
    console.log('🚀 Application initialized successfully');
}

// ============================================
// SCROLL & NAVIGATION
// ============================================

function initializeScrollIndicators() {
    const scrollIndicators = document.querySelectorAll('.scroll-indicator');
    scrollIndicators.forEach(indicator => {
        indicator.addEventListener('click', scrollToNextSection);
    });
}

function scrollToNextSection() {
    const heroSection = document.getElementById('hero');
    const sections = Array.from(document.querySelectorAll('section'));
    
    let nextSection = null;
    let foundHero = false;
    
    for (const section of sections) {
        if (foundHero && section.id !== 'hero') {
            nextSection = section;
            break;
        }
        if (section.id === 'hero') foundHero = true;
    }
    
    if (nextSection) {
        const offsetTop = nextSection.offsetTop - AppConfig.scrollOffset;
        
        // Fix animation conflicts and ensure smooth behavior
        const scrollIndicator = document.querySelector('.scroll-indicator');
        if (scrollIndicator) {
            // Clear any existing animations first
            scrollIndicator.style.animation = 'none';
            scrollIndicator.style.transition = 'none';
            
            // Immediate, smooth downward animation without delay
            setTimeout(() => {
                scrollIndicator.style.transform = 'scale(1.05) translateY(-2px)';
                scrollIndicator.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
                
                // Smooth arrow animation
                const scrollArrow = scrollIndicator.querySelector('.scroll-arrow');
                if (scrollArrow) {
                    scrollArrow.style.transform = 'translateY(0px) rotate(180deg)';
                    scrollArrow.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
                }
                
                // Clean reset after animation
                setTimeout(() => {
                    scrollIndicator.style.transform = 'scale(1) translateY(0px)';
                    if (scrollArrow) {
                        scrollArrow.style.transform = 'translateY(-2px) rotate(180deg)';
                    }
                }, 200);
            }, 50);
        }
        
        smoothScrollTo(offsetTop);
    }
}

function smoothScrollTo(targetPosition, duration = 800) {
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;
    
    function animation(currentTime) {
        if (!startTime) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);
        
        // Easing function for smooth animation
        const ease = easeInOutCubic(progress);
        window.scrollTo(0, startPosition + distance * ease);
        
        if (timeElapsed < duration) {
            requestAnimationFrame(animation);
        }
    }
    
    requestAnimationFrame(animation);
}

function easeInOutCubic(x) {
    return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
}

function initializeNavigation() {
    const navbar = document.getElementById('mainNav');
    if (!navbar) return;
    
    // Navbar scroll effect
    window.addEventListener('scroll', debounce(() => {
        navbar.classList.toggle('scrolled', window.scrollY > AppConfig.scrollThreshold);
    }, 10));
    
    // Smooth scrolling for all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', handleAnchorClick);
    });
    
    // Special handling for Get In Touch button
    setupGetInTouchButton();
}

function handleAnchorClick(e) {
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;
    
    const targetElement = document.querySelector(targetId);
    if (targetElement) {
        e.preventDefault();
        const offsetTop = targetElement.offsetTop - AppConfig.scrollOffset;
        smoothScrollTo(offsetTop);
        
        // Update URL without jumping
        history.pushState(null, null, targetId);
    }
}

function setupGetInTouchButton() {
    const buttonSelectors = [
        '#getInTouchBtn',
        'a[href="#feedback-contact-section"]',
        'a:contains("Get In Touch")'
    ];
    
    let getInTouchBtn = null;
    
    // Try to find by ID first
    getInTouchBtn = document.getElementById('getInTouchBtn');
    
    // If not found, try attribute selector
    if (!getInTouchBtn) {
        getInTouchBtn = document.querySelector('a[href="#feedback-contact-section"]');
    }
    
    // If still not found, try text content
    if (!getInTouchBtn) {
        const allLinks = Array.from(document.querySelectorAll('a'));
        getInTouchBtn = allLinks.find(link => link.textContent?.includes('Get In Touch'));
    }
    
    if (getInTouchBtn) {
        getInTouchBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.getElementById('feedback-contact-section');
            if (target) {
                const offsetTop = target.offsetTop - AppConfig.scrollOffset;
                smoothScrollTo(offsetTop);
            }
        });
    }
}

function initializeActiveNavigation() {
    const sections = Array.from(document.querySelectorAll('section[id]'));
    const navLinks = Array.from(document.querySelectorAll('.nav-link[href^="#"]'));
    
    if (sections.length === 0 || navLinks.length === 0) return;
    
    window.addEventListener('scroll', debounce(() => {
        let current = '';
        const scrollPosition = window.scrollY + AppConfig.scrollOffset + 50;
        
        for (const section of sections) {
            const sectionTop = section.offsetTop;
            const sectionBottom = sectionTop + section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                current = section.getAttribute('id');
                break;
            }
        }
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href')?.slice(1);
            if (href === current) {
                link.classList.add('active');
            }
        });
    }, 100));
}

// ============================================
// ANIMATIONS & VISUAL EFFECTS
// ============================================

function initializeAOS() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: AppConfig.aosDuration,
            once: true,
            offset: AppConfig.aosOffset,
            easing: 'ease-in-out',
            disable: window.innerWidth < 768 ? 'phone' : false
        });
    }
}

function initializeParticles() {
    const heroParticles = document.querySelector('.hero-particles');
    if (!heroParticles) return;
    
    setInterval(() => createParticle(heroParticles), 2000);
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.animationDelay = `${Math.random() * 20}s`;
    particle.style.animationDuration = `${15 + Math.random() * 10}s`;
    
    container.appendChild(particle);
    
    setTimeout(() => particle.remove(), 25000);
}

// ============================================
// PROJECTS SECTION
// ============================================

let currentProjectSlide = 0;
let totalProjectSlides = 0;
let projectsPerView = 3;
let isProjectAnimating = false;
let autoSlideInterval = null;

function initializeProjects() {
    // Initialize project filtering
    initializeProjectFilters();
    
    // Initialize projects slider
    const track = document.getElementById('projectsSliderTrack');
    if (track) {
        initializeProjectsSlider(track);
    }
}

function initializeProjectFilters() {
    const filterTabs = document.querySelectorAll('.project-tab');
    if (filterTabs.length === 0) return;
    
    filterTabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const category = tab.dataset.category;
            filterProjects(category);
        });
    });
}

function filterProjects(category) {
    // Update active tab
    const tabs = document.querySelectorAll('.project-tab');
    tabs.forEach(tab => {
        tab.classList.toggle('active', tab.dataset.category === category);
    });
    
    // Filter project cards
    const projectCards = document.querySelectorAll('.project-card');
    const projectsGrid = document.getElementById('projectsGrid');
    
    if (!projectsGrid) return;
    
    projectsGrid.classList.add('loading');
    
    let visibleCount = 0;
    
    projectCards.forEach((card, index) => {
        const cardCategory = card.dataset.category || 'web_dev';
        const shouldShow = category === 'all' || cardCategory === category;
        
        if (shouldShow) {
            card.style.display = '';
            card.style.opacity = '0';
            card.style.transform = 'scale(0.95)';
            visibleCount++;
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
            }, index * 50);
        } else {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.8)';
            setTimeout(() => {
                card.style.display = 'none';
            }, 300);
        }
    });
    
    setTimeout(() => {
        projectsGrid.classList.remove('loading');
        if (visibleCount === 0) {
            showEmptyState(category);
        } else {
            hideEmptyState();
        }
    }, 400);
}

function showEmptyState(category) {
    const projectsGrid = document.getElementById('projectsGrid');
    if (!projectsGrid) return;
    
    const existingEmpty = document.querySelector('.projects-grid-empty');
    if (existingEmpty) return;
    
    const emptyState = document.createElement('div');
    emptyState.className = 'projects-grid-empty';
    emptyState.innerHTML = `
        <i class="fas fa-folder-open"></i>
        <h3>No ${getCategoryName(category)} Projects</h3>
        <p>Check back soon for new projects in this category!</p>
    `;
    
    projectsGrid.appendChild(emptyState);
}

function hideEmptyState() {
    const emptyState = document.querySelector('.projects-grid-empty');
    if (emptyState) emptyState.remove();
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

function getCategoryIcon(category) {
    const icons = {
        'web_dev': '<i class="fas fa-laptop-code"></i>',
        'graphic_design': '<i class="fas fa-paint-brush"></i>',
        'video_editing': '<i class="fas fa-video"></i>'
    };
    return icons[category] || '<i class="fas fa-code"></i>';
}

function getCategoryBadge(category) {
    const badges = {
        'web_dev': '<i class="fas fa-code"></i> Web Dev',
        'graphic_design': '<i class="fas fa-palette"></i> Design',
        'video_editing': '<i class="fas fa-video"></i> Video'
    };
    return badges[category] || '<i class="fas fa-code"></i> Web Dev';
}

function initializeProjectsSlider(track) {
    const slides = document.querySelectorAll('.project-slide-item');
    if (!slides.length) return;
    
    totalProjectSlides = slides.length;
    updateProjectsPerView();
    updateProjectSliderControls();
    startAutoSlide();
    
    // Touch/swipe support
    setupTouchSupport(track, 'projects');
    
    // Pause on hover
    const wrapper = document.querySelector('.projects-slider-wrapper');
    if (wrapper) {
        wrapper.addEventListener('mouseenter', stopAutoSlide);
        wrapper.addEventListener('mouseleave', startAutoSlide);
    }
    
    // Handle resize
    window.addEventListener('resize', debounce(() => {
        updateProjectsPerView();
        updateProjectSliderControls();
        goToProjectSlide(currentProjectSlide, false);
    }, 250));
}

function updateProjectsPerView() {
    const width = window.innerWidth;
    if (width >= AppConfig.breakpoints.desktop) {
        projectsPerView = 3;
    } else if (width >= AppConfig.breakpoints.tablet) {
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
    const gap = 32;
    const offset = currentProjectSlide * (slideWidth + gap);
    
    if (animate) {
        isProjectAnimating = true;
        track.style.transform = `translateX(-${offset}px)`;
        setTimeout(() => { isProjectAnimating = false; }, 600);
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
    
    prevBtn.classList.toggle('disabled', currentProjectSlide === 0);
    nextBtn.classList.toggle('disabled', currentProjectSlide >= maxSlide);
    
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
    }, AppConfig.autoSlideDelay);
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

// ============================================
// SKILLS SLIDER
// ============================================

let currentSkillSlide = 0;
let totalSkillSlides = 0;
let skillsPerView = 4;
let isSkillAnimating = false;
let autoSkillSlideInterval = null;

function initializeSkillsSlider() {
    const track = document.getElementById('skillsSliderTrack');
    if (!track) return;
    
    const slides = document.querySelectorAll('.skill-slide-item');
    if (!slides.length) return;
    
    totalSkillSlides = slides.length;
    updateSkillsPerView();
    updateSkillSliderControls();
    startAutoSkillSlide();
    
    // Touch/swipe support
    setupTouchSupport(track, 'skills');
    
    // Pause on hover
    const wrapper = document.querySelector('#skills .projects-slider-wrapper');
    if (wrapper) {
        wrapper.addEventListener('mouseenter', stopAutoSkillSlide);
        wrapper.addEventListener('mouseleave', startAutoSkillSlide);
    }
    
    window.addEventListener('resize', debounce(() => {
        updateSkillsPerView();
        updateSkillSliderControls();
        goToSkillSlide(currentSkillSlide, false);
    }, 250));
}

function updateSkillsPerView() {
    const width = window.innerWidth;
    if (width >= AppConfig.breakpoints.desktop) {
        skillsPerView = 4;
    } else if (width >= AppConfig.breakpoints.tablet) {
        skillsPerView = 3;
    } else if (width >= AppConfig.breakpoints.mobile) {
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
    const gap = 32;
    const offset = currentSkillSlide * (slideWidth + gap);
    
    if (animate) {
        isSkillAnimating = true;
        track.style.transform = `translateX(-${offset}px)`;
        setTimeout(() => { isSkillAnimating = false; }, 600);
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
    
    prevBtn.classList.toggle('disabled', currentSkillSlide === 0);
    nextBtn.classList.toggle('disabled', currentSkillSlide >= maxSlide);
    
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
    }, AppConfig.skillSlideDelay);
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

// ============================================
// TESTIMONIALS SLIDER
// ============================================

function initializeTestimonialsSlider() {
    const swiperContainer = document.querySelector('.testimonialSwiper');
    if (!swiperContainer || typeof Swiper === 'undefined') return;
    
    const slides = swiperContainer.querySelectorAll('.swiper-slide');
    const slideCount = slides.length;
    
    const swiper = new Swiper('.testimonialSwiper', {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: false,
        autoplay: slideCount > 1 ? {
            delay: 5000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        } : false,
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
            640: { slidesPerView: 1, spaceBetween: 20 },
            768: { slidesPerView: 2, spaceBetween: 30 },
            1024: { slidesPerView: 2, spaceBetween: 40 },
            1200: { slidesPerView: 3, spaceBetween: 40 },
        },
        speed: 800,
        grabCursor: true,
        simulateTouch: true,
        touchRatio: 1,
        resistance: true,
        resistanceRatio: 0.85,
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') swiper.slidePrev();
        if (e.key === 'ArrowRight') swiper.slideNext();
    });
}

// ============================================
// NEWS SLIDER
// ============================================

let newsRefreshInterval = null;
let newsRequestInProgress = false;
let lastNewsRequestTime = 0;

function initializeNewsSlider() {
    const newsTrack = document.getElementById('newsSliderTrack');
    if (!newsTrack) return;
    
    fetchRecentProjects();
    newsRefreshInterval = setInterval(fetchRecentProjects, AppConfig.newsRefreshInterval);
    
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            clearInterval(newsRefreshInterval);
        } else {
            fetchRecentProjects();
            newsRefreshInterval = setInterval(fetchRecentProjects, AppConfig.newsRefreshInterval);
        }
    });
}

async function fetchRecentProjects() {
    if (newsRequestInProgress) return;
    
    const newsTrack = document.getElementById('newsSliderTrack');
    if (!newsTrack) return;
    
    newsRequestInProgress = true;
    lastNewsRequestTime = Date.now();
    
    try {
        const response = await fetch('/recent-projects');
        
        if (!response.ok) {
            if (response.status === 429) {
                console.log('Rate limit reached, backing off');
                await new Promise(resolve => setTimeout(resolve, 30000));
            }
            return;
        }
        
        const data = await response.json();
        
        if (data.success && data.projects?.length > 0) {
            renderNewsItems(data.projects);
        }
    } catch (error) {
        console.error('Error fetching recent projects:', error);
    } finally {
        newsRequestInProgress = false;
    }
}

function renderNewsItems(projects) {
    const newsTrack = document.getElementById('newsSliderTrack');
    if (!newsTrack) return;
    
    const createNewsItem = (project) => {
        const imageUrl = project.image 
            ? `/static/uploads/${project.image}` 
            : 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=100&h=100&fit=crop';
        
        const projectUrl = project.live_link || project.github_link || '#projects';
        
        return `
            <div class="news-item" onclick="window.open('${projectUrl}', '_blank')">
                <img src="${imageUrl}" alt="${escapeHtml(project.title)}" class="news-item-image" loading="lazy">
                <div class="news-item-content">
                    <h5 class="news-item-title">${escapeHtml(project.title)}</h5>
                    <p class="news-item-desc">${escapeHtml(project.short_description || project.description)}</p>
                    <span class="news-item-date">
                        <i class="fas fa-clock"></i>
                        ${project.created_at || 'Recently'}
                    </span>
                </div>
            </div>
        `;
    };
    
    const projectsHtml = projects.map(createNewsItem).join('');
    const duplicatedHtml = projects.length > 2 ? projectsHtml + projectsHtml : projectsHtml;
    
    newsTrack.innerHTML = duplicatedHtml;
    
    // Initialize Swiper
    const newsSliderWrapper = newsTrack.parentElement;
    if (typeof Swiper !== 'undefined' && newsSliderWrapper) {
        new Swiper(newsSliderWrapper, {
            slidesPerView: 1,
            spaceBetween: 20,
            loop: projects.length > 2,
            autoplay: { delay: 3000, disableOnInteraction: false, pauseOnMouseEnter: true },
            pagination: { el: '.swiper-pagination', clickable: true, dynamicBullets: true },
            navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
            breakpoints: { 640: { slidesPerView: 1 }, 768: { slidesPerView: 2 } }
        });
    }
}

// ============================================
// CONTACT FORM
// ============================================

function initializeContactForm() {
    const contactForm = document.getElementById('contactForm');
    if (!contactForm) return;
    
    const messageTextarea = document.getElementById('message');
    const charCount = document.getElementById('charCount');
    
    // Character counter
    if (messageTextarea && charCount) {
        messageTextarea.addEventListener('input', () => {
            const length = messageTextarea.value.length;
            charCount.textContent = length;
            
            if (length > AppConfig.maxMessageLength) {
                messageTextarea.value = messageTextarea.value.substring(0, AppConfig.maxMessageLength);
                charCount.textContent = AppConfig.maxMessageLength;
            }
            
            charCount.style.color = length > 400 ? '#e53e3e' : length > 300 ? '#ed8936' : '#a0aec0';
        });
    }
    
    // Real-time validation
    const inputs = contactForm.querySelectorAll('.form-control, .form-select');
    inputs.forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('input', () => clearFieldError(input));
    });
    
    // Form submission
    contactForm.addEventListener('submit', handleContactSubmit);
}

function validateField(field) {
    const feedback = field.parentElement.querySelector('.form-feedback');
    let isValid = true;
    let errorMessage = '';
    
    if (field.hasAttribute('required') && !field.value.trim()) {
        isValid = false;
        errorMessage = 'This field is required';
    } else if (field.type === 'email' && field.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    } else if (field.type === 'tel' && field.value) {
        const phoneRegex = /^[\d\s\-\+\(\)]+$/;
        if (!phoneRegex.test(field.value)) {
            isValid = false;
            errorMessage = 'Please enter a valid phone number';
        }
    }
    
    if (!isValid) {
        field.classList.add('is-invalid');
        if (feedback) {
            feedback.textContent = errorMessage;
            feedback.style.color = '#e53e3e';
        }
    } else {
        field.classList.remove('is-invalid');
        if (feedback) feedback.textContent = '';
    }
    
    return isValid;
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const feedback = field.parentElement.querySelector('.form-feedback');
    if (feedback) feedback.textContent = '';
}

function handleContactSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Validate all fields
    let isValid = true;
    const inputs = form.querySelectorAll('.form-control, .form-select');
    inputs.forEach(input => {
        if (!validateField(input)) isValid = false;
    });
    
    if (!isValid) {
        form.style.animation = 'shake 0.5s';
        setTimeout(() => { form.style.animation = ''; }, 500);
        return;
    }
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    
    const formData = new FormData(form);
    
    fetch('/contact', {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            form.reset();
            const charCount = document.getElementById('charCount');
            if (charCount) {
                charCount.textContent = '0';
                charCount.style.color = '#a0aec0';
            }
        } else {
            showNotification(data.message || 'Error sending message', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}

// ============================================
// FEEDBACK FORM
// ============================================

function initializeFeedbackForm() {
    const feedbackForm = document.getElementById('feedbackForm');
    if (!feedbackForm) return;
    
    // Avatar preview
    const avatarInput = document.getElementById('feedback_avatar');
    if (avatarInput) {
        avatarInput.addEventListener('change', handleAvatarPreview);
    }
    
    // Form submission
    feedbackForm.addEventListener('submit', handleFeedbackSubmit);
}

function handleAvatarPreview(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(event) {
        const avatarPreview = document.getElementById('avatar-preview');
        const avatarImg = document.getElementById('avatar-img');
        const uploadArea = document.querySelector('.upload-preview');
        
        if (avatarPreview) avatarPreview.style.display = 'block';
        if (avatarImg) avatarImg.src = event.target.result;
        if (uploadArea) uploadArea.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function handleFeedbackSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
    
    const formData = new FormData(form);
    
    fetch('/feedback', {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Feedback submitted successfully! Thank you!', 'success');
            form.reset();
            
            // Reset avatar preview
            const avatarPreview = document.getElementById('avatar-preview');
            const avatarImg = document.getElementById('avatar-img');
            const uploadArea = document.querySelector('.upload-preview');
            
            if (avatarPreview) avatarPreview.style.display = 'none';
            if (avatarImg) avatarImg.src = '';
            if (uploadArea) uploadArea.style.display = 'block';
        } else {
            showNotification(data.message || 'Error submitting feedback', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error submitting feedback. Please try again.', 'error');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}

// ============================================
// FOOTER & BACK TO TOP
// ============================================

function initializeFooter() {
    // Newsletter form
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleNewsletterSubmit);
    }
    
    // Footer links smooth scroll
    const footerLinks = document.querySelectorAll('.footer-link[href^="#"]');
    footerLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - AppConfig.scrollOffset;
                smoothScrollTo(offsetTop);
            }
        });
    });
}

function handleNewsletterSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const email = form.querySelector('.newsletter-input').value;
    const successDiv = document.getElementById('newsletterSuccess');
    
    if (email) {
        successDiv?.classList.add('show');
        form.reset();
        
        setTimeout(() => {
            successDiv?.classList.remove('show');
        }, 5000);
        
        // Send to server (implement as needed)
        console.log('Newsletter subscription:', email);
    }
}

function initializeBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', debounce(() => {
        backToTopBtn.classList.toggle('show', window.pageYOffset > 300);
    }, 100));
    
    backToTopBtn.addEventListener('click', () => {
        smoothScrollTo(0);
    });
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

function showNotification(message, type = 'success') {
    const existing = document.querySelector('.floating-notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = `floating-notification floating-notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
            <span>${escapeHtml(message)}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentElement) {
            notification.classList.add('notification-hiding');
            setTimeout(() => notification.remove(), 300);
        }
    }, AppConfig.notificationDuration);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

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

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function setupTouchSupport(track, sliderType) {
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    
    const navigate = sliderType === 'projects' ? navigateProjects : navigateSkills;
    
    track.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        isDragging = true;
        track.style.cursor = 'grabbing';
        if (sliderType === 'projects') stopAutoSlide();
        else stopAutoSkillSlide();
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
            navigate(diff > 0 ? 'next' : 'prev');
        } else {
            if (sliderType === 'projects') startAutoSlide();
            else startAutoSkillSlide();
        }
    });
}

function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }
}

function initializeResizeHandler() {
    let resizeTimer;
    window.addEventListener('resize', () => {
        document.body.classList.add('resize-animation-stopper');
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            document.body.classList.remove('resize-animation-stopper');
        }, 400);
    });
}

// ============================================
// EXPOSE GLOBAL FUNCTIONS FOR HTML
// ============================================

window.filterProjects = filterProjects;
window.refreshStats = refreshStats;
window.resetStats = resetStats;
window.debugStats = debugStats;
window.showNotification = showNotification;

// Stats functions (for admin panel)
function refreshStats() {
    if (confirm('Refresh statistics from database?')) {
        fetch('/admin/testimonials-stats/refresh', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showNotification('Statistics refreshed!', 'success');
                    location.reload();
                }
            })
            .catch(() => showNotification('Refresh failed', 'error'));
    }
}

function resetStats() {
    if (confirm('Reset all statistics to default? This cannot be undone.')) {
        fetch('/admin/testimonials-stats/reset', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (data.success) location.reload();
                else showNotification('Reset failed', 'error');
            });
    }
}

function debugStats() {
    console.log('Debug mode activated');
    showNotification('Debug info in console', 'info');
}

// ============================================
// INITIALIZE ON PAGE LOAD
// ============================================

document.addEventListener('DOMContentLoaded', initializeApp);