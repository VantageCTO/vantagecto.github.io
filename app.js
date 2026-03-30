
// Cursor
const cursor = document.getElementById('cursor');
const ring = document.getElementById('cursorRing');
document.addEventListener('mousemove', e => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
    setTimeout(() => {
        ring.style.left = e.clientX + 'px';
        ring.style.top = e.clientY + 'px';
    }, 60);
});

// Nav scroll
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);
});

// Scroll reveal
const reveals = document.querySelectorAll('.reveal');
const io = new IntersectionObserver((entries) => {
    entries.forEach((e, i) => {
        if (e.isIntersecting) {
            setTimeout(() => e.target.classList.add('visible'), 80 * (Array.from(reveals).indexOf(e.target) % 4));
            io.unobserve(e.target);
        }
    });
}, { threshold: 0.1 });
reveals.forEach(el => io.observe(el));



function closeModal() {
    document.getElementById('math-modal').classList.remove('open');
}
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeModal();
});
// Trap focus inside modal when open
document.getElementById('math-modal').addEventListener('keydown', function (e) {
    if (e.key !== 'Tab') return;
    const focusable = this.querySelectorAll('a, button, [tabindex]:not([tabindex="-1"])');
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (e.shiftKey ? document.activeElement === first : document.activeElement === last) {
        e.preventDefault();
        (e.shiftKey ? last : first).focus();
    }
});