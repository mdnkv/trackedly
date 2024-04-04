function removeEntry(id) {
    const message = gettext('Do you want to remove this entry?');

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
            const url = '/entries/api/delete/' + id + '/';

            fetch(url, config)
                .then(res => {
                    const entryElement = document.getElementById('app-entry-item-' + id);
                    entryElement.remove();
                    const successMessage = gettext('Entry was removed successfully!');
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


function setStartDateToday() {
    let input = document.getElementById('id_start_date');
    input.valueAsDate = new Date();
}
function setFinishDateToday() {
    let input = document.getElementById('id_finish_date');
    input.valueAsDate = new Date();
}
function setFinishDateAsStartDate() {
    let startDateInput = document.getElementById('id_start_date');
    let finishDateInput = document.getElementById('id_finish_date');
    finishDateInput.valueAsDate = startDateInput.valueAsDate;
}

function countEntryDescription(){
    let descriptionCount = document.getElementById('id_description').value.length;
    let counter = document.getElementById('app-description-counter');
    counter.innerText = descriptionCount + '/255';
    if (descriptionCount >= 200) {
        document.getElementById('id_description').classList.add('is-warning');
    } else {
        document.getElementById('id_description').classList.remove('is-warning');
    }
}