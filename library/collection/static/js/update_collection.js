(function () {
    document.querySelectorAll('.update-btn')
    .forEach(button => {
        button.addEventListener('click', () => {
            console.log('asdf');
            const updateUrl = button.dataset.updateUrl;
            options = {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            };
            fetch(updateUrl, options)
            .then(response => response.json())
            .then(data => {
                let modal = new bootstrap.Modal(document.getElementById('modal-book'));
                document.querySelector('#modal-book .modal-content').innerHTML = data.html_form;
                modal.show();
            });
        });  
    })
    document.addEventListener('submit', function(event) {
        if (event.target.classList.contains('js-update-collection-form')) {
            event.preventDefault();
            const form = event.target;
            const updateUrl = form.action;
            
            const formData = new FormData(form);
            options = {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: formData
            }
            fetch(updateUrl, options)
            .then(response => response.json())
            .then(data => {
                container = document.body.querySelector('.js-collection-content');
                container.innerHTML = data.html_collection_list;
                document.location.href = '/collection/add_collection/';
            })
            .catch(error => console.error(error));
        }
    });
})();