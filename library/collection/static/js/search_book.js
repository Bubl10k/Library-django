function handleAddRemoveBook(button, url, bookData, collectionId) {
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(bookData),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            let alertMessage = 'Book successfully added!';
            let container = document.createElement('div');
            container.classList.add('d-flex', 'justify-content-center', 'position-sticky');
            container.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show mt-1 w-75 sticky-top" role="alert">
                    ${alertMessage}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            parentDiv = document.body.querySelector('.content');
            parentDiv.insertBefore(container, parentDiv.firstChild);
            let rowDiv = button;
            for (let i = 0; i < 4; i++) {
                if (rowDiv.parentElement) {
                    rowDiv = rowDiv.parentElement;
                }
            }
            rowDiv.remove();
        } else {
            console.error(data.message);
        }
    })
    .catch(error => {
        let container = document.createElement('div');
        container.classList.add('d-flex', 'justify-content-center');
        container.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show mt-1 w-75" role="alert">
                There was an error processing your request. Please select a valid collection or try again later.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        parentDiv = document.body.querySelector('.content');
        parentDiv.insertBefore(container, parentDiv.firstChild);
    });
}


function addBookHandler(event, selectedCollectionUrl) {
    const button = event.target;
    const bookData = {
        title: button.dataset.title,
        author: button.dataset.author,
        num_pages: button.dataset.numPages,
        description: button.dataset.description,
    };
    handleAddRemoveBook(button, selectedCollectionUrl, bookData);
}


(function displayBooks() {
    const searchForm = document.querySelector('.seach-form');
    
    let selectElem = document.querySelector('.js-collection-url');
    let selectedCollectionUrl = null;
    let collectionId = null;
    selectElem.addEventListener('change', (event) => {
        selectedCollectionUrl = event.target.value;
        const selectedOption = event.target.selectedOptions[0];
        collectionId = selectedOption.dataset.collectionId; 
    });

    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const url = searchForm.dataset.searchUrl;
        console.log(url);
        let formData = new FormData(searchForm);
        const csrfToken = formData.get('csrfmiddlewaretoken');
        
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            let container = document.querySelector('#search-result');
            container.innerHTML = '';

            if (data) {
                data.items.forEach(item => {
                    const bookObj = item.volumeInfo;
                    if (!(bookObj.imageLinks && bookObj.imageLinks.smallThumbnail)) {
                        return;
                    }
                    let bookContainer = document.createElement('div');
                    bookContainer.classList.add('row');
                    let description = bookObj.description;
                    if (description && description.length > 2000) {
                        description = description.substring(0, 2000) + '...';
                    }
                    bookContainer.innerHTML = `
                        <div class="col mb-5">
                            <div class="d-flex justify-content-center pt-3">
                                <div>
                                    <img src="${bookObj.imageLinks.smallThumbnail}" class="rounded me-5" alt="${bookObj.title}" style="height:250px">
                                    <button type="button" class="btn btn-secondary mt-3 add-book-js" style="width: auto;" data-title="${bookObj.title}" data-author="${bookObj.authors}" data-num-pages="${bookObj.pageCount}" data-description="${description}">Add book</button>
                                </div>
                                <div>
                                    <h5><b>${bookObj.title}</b></h5>
                                    <p style="opacity: 0.40">${bookObj.authors}</p>
                                    <p><b>${bookObj.publishedDate} Pages:</b> ${bookObj.pageCount}</p>
                                    <p>${description}</p>
                    
                                </div>
                            </div>
                        </div>
                        <hr class="hr" />`;
                    container.appendChild(bookContainer);
                });
                
                let addButtons = document.querySelectorAll('.add-book-js');
                
                addButtons.forEach(button => {
                    button.addEventListener('click', (event) => addBookHandler(event, selectedCollectionUrl));
                });
            }
            
        })
        .catch(erorr => {
            let container = document.createElement('div');
            container.classList.add('d-flex', 'justify-content-center');
            container.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show mt-1 w-75 " role="alert">
                    There was an error processing your request. Please select a valid collection or try again later.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            parentDiv = document.body.querySelector('.content');
            parentDiv.insertBefore(container, parentDiv.firstChild);
        })

    })
})();