const mySiteUrl = 'http://127.0.0.1:8000/library/';

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.js-create-book').addEventListener('click', function() {
        fetch(mySiteUrl + 'create/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            let modal = new bootstrap.Modal(document.getElementById('modal-book'));
            document.querySelector('#modal-book .modal-content').innerHTML = data.html_form;
            modal.show();
            return document.querySelector('.js-create-book-form')
        })
        .then(form => {
            form.addEventListener('submit', function (event) {
                event.preventDefault();
                let formData = new FormData(this);
                let url = this.action;
                
                let options = {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                }

                fetch(url, options)
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Invalid response');  
                    }
                })
                .then(data => {
                    if (data.status) {
                        document.body.innerHTML = data.html_book_list;
                        window.location.replace(mySiteUrl);
                    } else {
                        throw new Error('Invalid json');
                    }
                })
                .catch(error => console.error(error));
            });
        })
    });
});
