function sendEmailConfirmation() {
    const csrfToken = getCsrfToken();

    const config = {
        method: 'POST',
        mode: 'same-origin',
        headers: {'X-CSRFToken': csrfToken}
    }
    const url = '/users/api/email-confirm/';

    fetch(url, config)
        .then(result => {
            const message = gettext('Email confirmation was sent. Please check your inbox');
            swal(message, {icon: 'success'});
        })
        .catch(err => {
            console.log(err);
            const errorMessage = gettext('Something went wrong! Please try again');
            swal(errorMessage, {icon: 'error'});
        });
}