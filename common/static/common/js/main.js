document.addEventListener('DOMContentLoaded', function () {
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const navUl = document.querySelector('.navbar ul');

    if (hamburgerMenu && navUl) {
        hamburgerMenu.addEventListener('click', function () {
            navUl.classList.toggle('active');  // when user clicks add active class on the nav <ul>
        });
    }
});
