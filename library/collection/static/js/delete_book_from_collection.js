'use strict';

(function () {
    function attachDeleteHandlers () {
        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', () => {
                const deleteUrl = button.dataset.deleteUrl;
                let options = {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        
                    },
                }
                let modal = null;
    
                fetch(deleteUrl, options)
                .then(response => response.json())
                .then(data => {
                    modal = new bootstrap.Modal(document.getElementById('modal-book'));
                    document.querySelector('#modal-book .modal-content').innerHTML = data.html_confirm;
                    modal.show();
                    return document.querySelector('.delete-confirm-form');
                })
                .then(form => {
                    form.addEventListener('submit', function (event) {
                        event.preventDefault();
                        let formData = new FormData(form);
                        let postOptions = {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-Requested-With': 'XMLHttpRequest',
                                'X-CSRFToken': getCookie('csrftoken'),
                            },
                        }
                        fetch(deleteUrl, postOptions)
                        .then(response => response.json())
                        .then(data => {
                            modal.hide();
                            let container = document.querySelector('.container.mt-4');
                            if (container) {
                                container.innerHTML = data.html_books_list;
                                attachDeleteHandlers();
                            } else {
                                throw new Error('Invalid response');
                            }
                        })
                    })
                })
                .catch(err => {
                    console.error(err.message);})
            })
        })
    }
    
    attachDeleteHandlers();
}) ();
