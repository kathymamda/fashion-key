document.addEventListener('DOMContentLoaded', () => {
    // Header Scroll Effect
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Simple Animation Trigger on Scroll
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .section-title').forEach(el => {
        observer.observe(el);
    });

    // Mock Body Analysis Form
    const bodyForm = document.getElementById('body-analysis-form');
    if (bodyForm) {
        bodyForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Análisis procesado por la IA de Fashion Key (Simulación)');
            window.location.href = '/dashboard';
        });
    }

    // Simulator Interaction (Mock)
    const simulatorItems = document.querySelectorAll('.simulator-item');
    if (simulatorItems) {
        simulatorItems.forEach(item => {
            item.addEventListener('click', () => {
                const type = item.dataset.type;
                const preview = document.getElementById('avatar-preview');
                if (preview) {
                    preview.innerHTML = `<div class="placeholder-outfit">Outfit de ${type} seleccionado</div>`;
                }
            });
        });
    }
});
