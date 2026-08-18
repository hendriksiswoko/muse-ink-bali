document.getElementById('year').textContent = new Date().getFullYear();

const heroVideo = document.querySelector('.hero-video');
if (heroVideo && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  heroVideo.pause();
  heroVideo.removeAttribute('autoplay');
}

const navToggle = document.getElementById('nav-toggle');
const mainNav = document.getElementById('main-nav');

navToggle.addEventListener('click', () => {
  const isOpen = mainNav.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(isOpen));
});

mainNav.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    mainNav.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  });
});

// Text reveal + stagger
document.querySelectorAll('[data-split-words]').forEach(el => {
  const words = el.textContent.trim().split(/\s+/);
  el.innerHTML = words
    .map(word => `<span class="reveal-line"><span class="reveal-word">${word}</span></span>`)
    .join(' ');
});

document.querySelectorAll('.reveal-section .service-card').forEach((card, i) => {
  card.style.transitionDelay = `${i * 1000}ms`;
});

const revealSections = document.querySelectorAll('.reveal-section');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in-view');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.2 });

revealSections.forEach(section => revealObserver.observe(section));
