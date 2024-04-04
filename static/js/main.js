function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getCsrfToken(){
    return getCookie('csrftoken');
}

function submitLogoutForm() {
    const logoutMessage = gettext('Do you want to logout?');
    swal({
        text: logoutMessage,
        icon: 'info',
        buttons: true
    }).then(isLogout => {
        if (isLogout) {
            const form = document.getElementById('app-logout-form');
            form.submit();
        }
    });
}

function toggleNavbarBtn() {
    const navbarBtn = document.getElementById('app-navbar-btn');
    const navbarMenu = document.getElementById('app-navbar-menu');
    navbarBtn.classList.toggle('is-active');
    navbarMenu.classList.toggle('is-active');
}