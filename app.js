
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
const API_URL = 'https://vantage-api.fly.dev';

async function submitEmail(inputId, successId, formId) {
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

    const btn = form.querySelector('.email-btn');
    btn.disabled = true;
    btn.textContent = 'Submitting…';

    try {
        const res = await fetch(`${API_URL}/waitlist/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, source: 'website' }),
        });

        if (res.ok) {
            form.style.display = 'none';
            success.style.display = 'block';
        } else {
            const data = await res.json().catch(() => null);
            if (res.status === 409) {
                form.style.display = 'none';
                success.textContent = '\u2713 You\u2019re already on the list!';
                success.style.display = 'block';
            } else if (res.status === 429) {
                showFormError(input, btn, 'Too many requests. Please try again shortly.');
            } else {
                showFormError(input, btn, data?.detail || 'Something went wrong. Please try again.');
            }
        }
    } catch {
        showFormError(input, btn, 'Network error. Please check your connection and try again.');
    }
}

function showFormError(input, btn, message) {
    input.style.borderBottom = '1px solid #ff4444';
    btn.disabled = false;
    btn.textContent = btn.closest('#heroForm') ? 'Get Early Access' : 'Claim My Spot';
    const note = input.closest('.email-form-wrap, .final-form-wrap')?.querySelector('.form-note');
    if (note) {
        note.dataset.original = note.dataset.original || note.textContent;
        note.textContent = message;
        note.style.color = '#ff4444';
        setTimeout(() => {
            note.textContent = note.dataset.original;
            note.style.color = '';
            input.style.borderBottom = '';
        }, 3000);
    }
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
