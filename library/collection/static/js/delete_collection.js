(function () {
    function attachDeleteHandlers() {
        let modal = null;

        document.querySelectorAll('.delete-btn')
        .forEach(button => {
            button.addEventListener('click', () => {
                const deleteUrl = button.dataset.deleteUrl;
                console.log(deleteUrl);
                options = {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                };
                fetch(deleteUrl, options)
                .then(response => response.json())
                .then(data => {
                    modal = new bootstrap.Modal(document.getElementById('modal-book'));
                    document.querySelector('#modal-book .modal-content').innerHTML = data.html_form;
                    modal.show();
                });
            });  
        })
        document.addEventListener('submit', function(event) {
            if (event.target.classList.contains('js-delete-collection-form')) {
                event.preventDefault();
                const form = event.target;
                const deleteUrl = form.action;
                
                const formData = new FormData(form);
                options = {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: formData
                }
                fetch(deleteUrl, options)
                .then(response => response.json())
                .then(data => {
                    container = document.body.querySelector('.js-collection-content');
                    container.innerHTML = data.html_collection_list;
                    modal.hide();
                    attachDeleteHandlers();
                })
                .catch(error => console.error(error));
            }
        });
    }
    attachDeleteHandlers();
})();