// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function (message) {
        setTimeout(function () {
            message.style.animation = 'slideOut 0.3s ease-in forwards';
            setTimeout(function () {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Confirmation for delete actions
function confirmDelete(itemName) {
    return confirm(`¿Estás seguro de que deseas eliminar "${itemName}"?`);
}

// Image preview functionality (already in form template but can be here too)
function setupImagePreview() {
    const imageInput = document.getElementById('imagen');
    if (!imageInput) return;

    imageInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        const preview = document.getElementById('imagePreview');
        const fileText = document.querySelector('.file-text');

        if (file) {
            fileText.textContent = file.name;

            const reader = new FileReader();
            reader.onload = function (e) {
                preview.innerHTML = `
                    <p class="text-sm">Vista previa:</p>
                    <img src="${e.target.result}" alt="Preview" class="preview-image">
                `;
            };
            reader.readAsDataURL(file);
        } else {
            fileText.textContent = 'Seleccionar imagen...';
            preview.innerHTML = '';
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', setupImagePreview);

// Smooth scroll for anchor links
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

// Add loading state to forms on submit
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function (e) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn && !form.hasAttribute('onsubmit')) {
            submitBtn.disabled = true;
            submitBtn.style.opacity = '0.6';
            submitBtn.innerHTML = '⏳ Procesando...';
        }
    });
});
