
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

// Email submission
function submitEmail(inputId, successId, formId) {
    const input = document.getElementById(inputId);
    const success = document.getElementById(successId);
    const form = document.getElementById(formId);
    const email = input.value.trim();
    if (!email || !email.includes('@')) {
        input.style.borderBottom = '1px solid #ff4444';
        input.focus();
        setTimeout(() => input.style.borderBottom = '', 1500);
        return;
    }
    form.style.display = 'none';
    success.style.display = 'block';
    console.log('Email captured:', email);
    // Connect your email backend here (Resend, ConvertKit, etc.)
}

// Allow Enter key on email inputs
document.querySelectorAll('.email-input').forEach(input => {
    input.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
            const btn = input.nextElementSibling;
            if (btn) btn.click();
        }
    });
});
