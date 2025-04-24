// Mobile Menu Toggle
const menuBtn = document.getElementById('menuBtn');
const nav = document.getElementById('navbar');

menuBtn.addEventListener('click', () => {
    nav.classList.toggle('nav-active');
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!nav.contains(e.target) && nav.classList.contains('nav-active')) {
        nav.classList.remove('nav-active');
    }
});

// Particles Animation
const particlesContainer = document.getElementById('particles');
const particleCount = 50;

for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    const size = Math.random() * 4 + 2;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.animationDelay = `${Math.random() * 15}s`;
    particlesContainer.appendChild(particle);
}

// Testimonial Slider
const testimonialSlides = document.querySelector('.testimonial-slides');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
let currentSlide = 0;

function updateSlider() {
    testimonialSlides.style.transform = `translateX(-${currentSlide * 100}%)`;
}

prevBtn.addEventListener('click', () => {
    currentSlide = (currentSlide - 1 + testimonialSlides.children.length) % testimonialSlides.children.length;
    updateSlider();
});

nextBtn.addEventListener('click', () => {
    currentSlide = (currentSlide + 1) % testimonialSlides.children.length;
    updateSlider();
});

setInterval(() => {
    currentSlide = (currentSlide + 1) % testimonialSlides.children.length;
    updateSlider();
}, 5000);

// Scroll Animation
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.feature-card, .step-content, .testimonial, .stat-card, .scan-card');
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        if (elementPosition < screenPosition) {
            element.classList.add('fade-in-up');
        }
    });
};

window.addEventListener('scroll', animateOnScroll);

// Initialize animations on page load
document.addEventListener('DOMContentLoaded', () => {
    animateOnScroll();

    // Quick URL Analysis
    const quickUrlForm = document.getElementById('quickUrlForm');
    const quickUrlInput = document.getElementById('quickUrlInput');
    const quickResult = document.getElementById('quickResult');

    if (quickUrlForm) {
        quickUrlForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = quickUrlInput.value.trim();
            if (!url) {
                quickResult.textContent = 'Please enter a URL';
                quickResult.className = 'quick-result error';
                quickResult.classList.add('show');
                setTimeout(() => quickResult.classList.remove('show'), 3000);
                return;
            }

            quickResult.textContent = 'Analyzing...';
            quickResult.className = 'quick-result';
            quickResult.classList.add('show');

            try {
                // Simulate API call
                await new Promise(resolve => setTimeout(resolve, 1000));
                const response = {
                    status: 'safe',
                    details: {
                        domainAge: '2 years',
                        sslStatus: 'Valid'
                    }
                };

                quickResult.innerHTML = `
                    <p><i class="fas fa-shield-alt"></i> Status: <span class="status ${response.status}">${response.status.charAt(0).toUpperCase() + response.status.slice(1)}</span></p>
                    <p>Domain Age: ${response.details.domainAge}</p>
                    <p>SSL: ${response.details.sslStatus}</p>
                `;
            } catch (error) {
                quickResult.textContent = 'Error analyzing URL';
                quickResult.className = 'quick-result error';
                setTimeout(() => quickResult.classList.remove('show'), 3000);
            }
        });
    }

    // Animated Percentage Circles
    const circles = document.querySelectorAll('.progress-circle');
    circles.forEach(circle => {
        const percentage = circle.dataset.percentage;
        const progress = circle.querySelector('.progress');
        const value = circle.querySelector('.progress-value');
        let current = 0;

        const animate = () => {
            if (current <= percentage) {
                value.textContent = `${Math.round(current)}%`;
                const offset = 377 - (377 * current) / 100;
                progress.style.strokeDashoffset = offset;
                current += 0.5;
                requestAnimationFrame(animate);
            }
        };
        animate();
    });

    // Animated Counters
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = parseFloat(counter.dataset.target);
        let current = 0;
        const increment = target / 100;

        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = current.toFixed(target % 1 === 0 ? 0 : 1);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toFixed(target % 1 === 0 ? 0 : 1);
            }
        };
        updateCounter();
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
            if (nav.classList.contains('nav-active')) {
                nav.classList.remove('nav-active');
            }
        }
    });
});

// Newsletter Form Submission
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const emailInput = newsletterForm.querySelector('input[type="email"]');
        const email = emailInput.value;
        console.log('Subscribing email:', email);
        const successMessage = document.createElement('div');
        successMessage.classList.add('success-message');
        successMessage.textContent = 'Thank you for subscribing!';
        newsletterForm.appendChild(successMessage);
        emailInput.value = '';
        setTimeout(() => {
            successMessage.remove();
        }, 3000);
    });
}

// Navbar scroll effect
let lastScroll = 0;
window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll <= 0) {
        nav.classList.remove('scroll-up');
        return;
    }
    if (currentScroll > lastScroll && !nav.classList.contains('scroll-down')) {
        nav.classList.remove('scroll-up');
        nav.classList.add('scroll-down');
    } else if (currentScroll < lastScroll && nav.classList.contains('scroll-down')) {
        nav.classList.remove('scroll-down');
        nav.classList.add('scroll-up');
    }
    lastScroll = currentScroll;
});