
// Page Navigation
const navLinks = document.querySelectorAll('.nav-link');
const pages = document.querySelectorAll('.page');
const footerLinks = document.querySelectorAll('footer a[data-page]');
const ctaButtons = document.querySelectorAll('.cta-button[data-page]');

function showPage(pageId) 
  // Hide all pages
  pages.forEach(page => {
    page.classList.remove('active');
  });

  // Show selected page
  const targetPage = document.getElementById(pageId);
  if (targetPage) {
    targetPage.classList.add('active');
  }

  // Update active nav link
  navLinks.forEach(link => {
    link.classList.remove('active');
  });

  const activeLink = document.querySelector(`[data-page="${pageId}"]`);
  if (activeLink && activeLink.classList.contains('nav-link')) {
    activeLink.classList.add('active');
  }

  // Close mobile menu
  document.getElementById('nav-menu').classList.remove('active');

  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });

  // Trigger scroll reveal animations
  setTimeout(() => {
    revealElements();
  }, 100);
}

// Add click listeners to navigation links
navLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const pageId = link.getAttribute('data-page');
    showPage(pageId);
  });
});

// Add click listeners to footer links
footerLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const pageId = link.getAttribute('data-page');
    showPage(pageId);
  });
});

// Add click listeners to CTA buttons
ctaButtons.forEach(button => {
  button.addEventListener('click', (e) => {
    e.preventDefault();
    const pageId = button.getAttribute('data-page');
    showPage(pageId);
  });
});

// Mobile Menu Toggle
const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
const navMenu = document.getElementById('nav-menu');

mobileMenuToggle.addEventListener('click', () => {
  navMenu.classList.toggle('active');
});

// Navbar scroll effect
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
  if (window.scrollY > 100) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// Scroll reveal animation
function revealElements() {
  const reveals = document.querySelectorAll('.scroll-reveal');

  reveals.forEach(element => {
    const windowHeight = window.innerHeight;
    const elementTop = element.getBoundingClientRect().top;
    const elementVisible = 150;

    if (elementTop < windowHeight - elementVisible) {
      element.classList.add('revealed');
    }
  });
}

window.addEventListener('scroll', revealElements);

// Initial reveal
revealElements();

// Form submissions
document.getElementById('booking-form').addEventListener('submit', (e) => {
  e.preventDefault();

  // Get form data
  const formData = new FormData(e.target);
  const bookingData = Object.fromEntries(formData);

  // Simulate booking process
  alert('Thank you for your booking request! We will contact you shortly to confirm your reservation.');

  // Reset form
  e.target.reset();
});

document.getElementById('contact-form').addEventListener('submit', (e) => {
  e.preventDefault();

  // Get form data
  const formData = new FormData(e.target);
  const contactData = Object.fromEntries(formData);

  // Simulate contact form submission
  alert('Thank you for your message! We will get back to you within 24 hours.');

  // Reset form
  e.target.reset();
});

// Room booking buttons
document.querySelectorAll('.book-button').forEach(button => {
  button.addEventListener('click', () => {
    // Get room type from the card
    const roomCard = button.closest('.room-card');
    const roomTitle = roomCard.querySelector('.room-title').textContent;

    // Switch to booking page
    showPage('bookings');

    // Pre-select room type in form
    setTimeout(() => {
      const roomSelect = document.getElementById('room-type');
      const roomValue = roomTitle.toLowerCase().replace(/\s+/g, '-').replace('suite', '').replace('room', '').trim();

      // Map room titles to select values
      const roomMap = {
        'presidential': 'presidential',
        'executive': 'executive',
        'deluxe': 'deluxe',
        'garden': 'garden',
        'standard': 'standard',
        'penthouse': 'penthouse'
      };

      for (const [key, value] of Object.entries(roomMap)) {
        if (roomTitle.toLowerCase().includes(key)) {
          roomSelect.value = value;
          break;
        }
      }

      // Set default check-in date to today
      const today = new Date().toISOString().split('T')[0];
      document.getElementById('checkin').value = today;

      // Set default check-out date to tomorrow
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      document.getElementById('checkout').value = tomorrow.toISOString().split('T')[0];
    }, 100);
  });
});

// Set minimum dates for booking form
const today = new Date().toISOString().split('T')[0];
document.getElementById('checkin').min = today;
document.getElementById('checkout').min = today;

// Update checkout minimum date when checkin changes
document.getElementById('checkin').addEventListener('change', (e) => {
  const checkinDate = new Date(e.target.value);
  checkinDate.setDate(checkinDate.getDate() + 1);
  document.getElementById('checkout').min = checkinDate.toISOString().split('T')[0];
});

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Add loading animation for page transitions
function addLoadingAnimation() {
  const pages = document.querySelectorAll('.page');
  pages.forEach(page => {
    page.style.opacity = '0';
    page.style.transform = 'translateY(20px)';

    setTimeout(() => {
      page.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      page.style.opacity = '1';
      page.style.transform = 'translateY(0)';
    }, 100);
  });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  addLoadingAnimation();
  revealElements();
});

// Add hover effects for room cards
document.querySelectorAll('.room-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    card.style.transform = 'translateY(-10px) scale(1.02)';
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'translateY(0) scale(1)';
  });
});

// Add parallax effect to hero section
window.addEventListener('scroll', () => {
  const hero = document.querySelector('.hero');
  if (hero && document.getElementById('home').classList.contains('active')) {
    const scrolled = window.pageYOffset;
    const rate = scrolled * -0.5;
    hero.style.transform = `translateY(${rate}px)`;
  }
});

// Add intersection observer for better performance
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
    }
  });
}, observerOptions);

// Observe all scroll-reveal elements
document.querySelectorAll('.scroll-reveal').forEach(el => {
  observer.observe(el);
});
