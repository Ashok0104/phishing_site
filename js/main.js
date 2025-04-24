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
    
    // Random size between 2px and 6px
    const size = Math.random() * 4 + 2;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    
    // Random position
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    
    // Random animation delay
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

// Auto-rotate testimonials
setInterval(() => {
    currentSlide = (currentSlide + 1) % testimonialSlides.children.length;
    updateSlider();
}, 5000);

// Scroll Animation
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.feature-card, .step-content, .testimonial');
    
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
            
            // Close mobile menu if open
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
        
        // Here you would typically send the email to your server
        console.log('Subscribing email:', email);
        
        // Show success message
        const successMessage = document.createElement('div');
        successMessage.classList.add('success-message');
        successMessage.textContent = 'Thank you for subscribing!';
        newsletterForm.appendChild(successMessage);
        
        // Clear input
        emailInput.value = '';
        
        // Remove success message after 3 seconds
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
        // Scroll down
        nav.classList.remove('scroll-up');
        nav.classList.add('scroll-down');
    } else if (currentScroll < lastScroll && nav.classList.contains('scroll-down')) {
        // Scroll up
        nav.classList.remove('scroll-down');
        nav.classList.add('scroll-up');
    }
    
    lastScroll = currentScroll;
}); 