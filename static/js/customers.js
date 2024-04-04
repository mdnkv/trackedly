function removeCustomer(id) {
    const message = gettext('Do you want to remove this customer?');

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
            const url = '/customers/api/delete/' + id + '/';

            fetch(url, config)
                .then(res => {
                    const customerElement = document.getElementById('app-customer-item-' + id);
                    customerElement.remove();
                    const successMessage = gettext('Customer was removed successfully!');
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