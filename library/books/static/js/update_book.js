(function() {
    document.querySelectorAll('.update-btn').forEach(button => {
        button.addEventListener('click', function() {
            fetch(this.dataset.bookUrl, {
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
            });
        });
    });

    document.addEventListener('submit', function(event) {
        if (event.target.classList.contains('js-update-book-form')) {
            event.preventDefault();
            const form = event.target;
            const url = form.action;
            const formData = new FormData(form);
            const options = {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: formData
            };
            fetch(url, options)
            .then(response => response.json())
            .then(data => {
                let container = document.querySelector('.container.mt-4');
                if (container) {
                    container.innerHTML = data.html_book_list;
                    document.location.href = '/library/'
                } else {
                    container = document.createElement('div');
                    container.classList.add('container', 'mt-4');
                    container.innerHTML = data.html_book_list;
                    document.body.appendChild(container);
                }
            })
            .catch(err => {
                console.error('Fetch error:', err);
            });
        }
    });
})();