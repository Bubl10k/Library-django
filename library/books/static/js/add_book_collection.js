(function () {
    document.querySelectorAll('.collection-btn')
    .forEach(btn => {
        let modal = new bootstrap.Modal(document.getElementById('modal-book'));
        btn.addEventListener('click', (event) => {
            event.preventDefault();
            const url = btn.dataset.bookUrl;
            const options = {
                method: 'GET',
                header: {
                    'Content-Type': 'application/json',
                }
            }
            fetch(url, options)
            .then(response => response.json())
            .then(data => {
                document.querySelector('#modal-book .modal-content').innerHTML = data.html_form;
                modal.show();
                return document.querySelector('.js-collection-book-form');
            })
            .then(form => {
                form.addEventListener('submit', (event) => {
                    event.preventDefault();
                    const formData = new FormData(form);
                    const url = form.action;
                    const options = {
                        method: 'POST',
                        body: formData
                    }
                    fetch(url, options)
                    .then(response => response.json())
                    .then(data => {
                        if (data.status) {
                            modal.hide();
                            let container = document.createElement('div');
                            container.classList.add('d-flex', 'justify-content-center');
                            container.innerHTML = `
                                <div class="alert alert-success alert-dismissible fade show mt-1 w-75 sticky-top" role="alert">
                                    Book successfully added to collection!
                                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>
                            `;
                            parentDiv = document.body.querySelector('.content');
                            parentDiv.insertBefore(container, parentDiv.firstChild);
                        } else {
                            // for debug
                            throw new Error('Invalid data');
                        }
                    })
                    .catch(error => console.error(error));
                })
            })
        })
    });
}) ();
