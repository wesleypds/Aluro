document.addEventListener('DOMContentLoaded', function () {
    const loginLink = document.getElementById('login-link');
    const cadastroLink = document.getElementById('cadastro-link');
    const loginSection = document.getElementById('login');
    const cadastroSection = document.getElementById('cadastro');
    const filter = document.getElementById('filter');
    const courseCards = document.querySelectorAll('.course-card');
    const btnScroll = document.querySelector('.btn-scroll');

    loginLink.addEventListener('click', function (e) {
        e.preventDefault();
        loginSection.classList.toggle('hidden');
        cadastroSection.classList.add('hidden');
    });

    cadastroLink.addEventListener('click', function (e) {
        e.preventDefault();
        cadastroSection.classList.toggle('hidden');
        loginSection.classList.add('hidden');
    });

    filter.addEventListener('change', function () {
        const selectedCategory = this.value;
        courseCards.forEach(function (card) {
            if (selectedCategory === 'all') {
                card.style.display = 'block';
            } else {
                if (card.classList.contains(selectedCategory)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            }
        });
    });

    // Inicializa o filtro para mostrar todos os cursos
    filter.dispatchEvent(new Event('change'));

    // Rolagem suave ao clicar no botão "Nossos cursos"
    btnScroll.addEventListener('click', function (e) {
        e.preventDefault();
        const cursosSection = document.getElementById('cursos');
        cursosSection.scrollIntoView({ behavior: 'smooth' });
    });
});
