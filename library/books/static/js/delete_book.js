document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            fetch(this.dataset.bookUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                let modal = new bootstrap.Modal(document.getElementById('modal-book'));
                document.querySelector('#modal-book .modal-content').innerHTML = data.html_confirm;
                modal.show();
                return document.querySelector('.delete-confirm-form');
            })
            .then(form => {
                form.addEventListener('submit', function (event) {
                    event.preventDefault();
                    let formData = new FormData(form);
                    let options = {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                    }
                    fetch(this.action, options)
                    .then(response => response.json())
                    .then(data => {
                        document.innerHTML = data.html_book_list;
                        window.location.replace(mySiteUrl);
                    })
                    .catch(error => console.error(error));
                });
            });
        });
    });
});
