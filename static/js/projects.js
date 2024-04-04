function removeProject(id) {
    const message = gettext('Do you want to remove this project?');

    swal({
        text: message,
        icon: 'warning',
        buttons: true,
        dangerMode: true
    }).then(isConfirmed => {
        if (isConfirmed) {
            const csrfToken = getCsrfToken();

            const config = {
                method: 'DELETE',
                mode: 'same-origin',
                headers: {'X-CSRFToken': csrfToken}
            }
            const url = '/projects/api/delete/' + id + '/';

            fetch(url, config)
                .then(res => {
                    const projectElement = document.getElementById('app-project-item-' + id);
                    projectElement.remove();
                    const successMessage = gettext('Project was removed successfully!');
                    swal(successMessage, {icon: 'success'});
                })
                .catch(err => {
                    console.log(err);
                    const errorMessage = gettext('Something went wrong! Please try again');
                    swal(errorMessage, {icon: 'error'});
                })
        }
    });
}