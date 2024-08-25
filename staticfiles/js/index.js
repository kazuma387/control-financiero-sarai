// navbar
const toggle = document.querySelector('.toggle')
const links = document.querySelector('.links')

toggle.addEventListener('click', () => {
    toggle.classList.toggle('rotate')
    links.classList.toggle('active')
})

// mensaje de success
document.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(() => {
        let messages = document.querySelector('.alert-success');
        if (messages) {
            messages.style.transition = 'opacity 0.5s ease-out';
            messages.style.opacity = '0';
            setTimeout(() => {
                messages.remove();
            }, 500);
        }
    }, 3000); // 3000ms = 3 seconds
});


// mensaje de delete
document.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(() => {
        let messages = document.querySelector('.alert-delete');
        if (messages) {
            messages.style.transition = 'opacity 0.5s ease-out';
            messages.style.opacity = '0';
            setTimeout(() => {
                messages.remove();
            }, 500);
        }
    }, 3000); // 3000ms = 3 seconds
});



