(function () {
    const baseUrl = '/collection/get_books/';
    let selectElem = document.querySelector('.js-collection-url');
    let selectedCollectionUrl = null;
    let collectionId = null;

    selectElem.addEventListener('change', (event) => {
        selectedCollectionUrl = event.target.value;
        const selectedOption = event.target.selectedOptions[0];
        collectionId = selectedOption.dataset.collectionId;
    })

    document.querySelector('.js-collection-books')
    .addEventListener('click', (e) => {
        e.preventDefault();
        if (!collectionId) {
            let container = document.createElement('div');
            container.classList.add('d-flex', 'justify-content-center');
            container.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show mt-1 w-75" role="alert">
                    Select a valid collection
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            parentDiv = document.body.querySelector('.content');
            parentDiv.insertBefore(container, parentDiv.firstChild);
            return;
        }

        let url = baseUrl + collectionId + '/';

        options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }
        fetch(url, options)
        .then(response => response.json())
        .then(data => {
            const container = document.body.querySelector('.container');
            let closeButtonHtml = `
                <div class="text-center mt-3 mb-3">
                    <button type="button" class="btn btn-primary js-close-collection">Hide collection list</button>
                </div>
            `
            if (container) {
                container.innerHTML = data.collection + closeButtonHtml;
            } else {
                const newContainer = document.createElement('div');
                newContainer.classList.add('container');
                newContainer.innerHTML = data.collection + closeButtonHtml;
                document.body.appendChild(newContainer);
            }
            const sources = document.querySelector('.js-collection-books').dataset;
            const updateSrc = sources.updateSrc
            const deleteSrc = sources.deleteSrc;
            const collectionSrc = sources.collectionSrc;
            if (updateSrc) {
                let updateScript = document.createElement('script');
                updateScript.src = updateSrc;
                document.body.querySelector('.content').appendChild(updateScript);
            }
            if (deleteSrc) {
                let deleteScript = document.createElement('script');
                deleteScript.src = deleteSrc;
                document.body.querySelector('.content').appendChild(deleteScript);
            }
            if (collectionSrc) {
                let collectionScript = document.createElement('script');
                collectionScript.src = collectionSrc;
                document.body.querySelector('.content').appendChild(collectionScript);
            }
        })
        .catch((err) => {
            console.error(err.message);
        })
    })
})();
