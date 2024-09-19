(function () {
    let form = document.querySelector('.js-add-collection')

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        let formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            let container = document.createElement('div');
            container.classList.add('d-flex', 'justify-content-center');
            container.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show mt-1 w-75 sticky-top" role="alert">
                    Collection successfully added!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            parentDiv = document.body.querySelector('.content');
            parentDiv.insertBefore(container, parentDiv.firstChild);
            let cartContainer = document.body.querySelector('.js-collection-content');
            cartContainer.innerHTML = data.html_collection_list;
        })
        .catch(error => {
            console.error('Error add collection:', error);
        });
        
    });
}) ();
