(function () {
    document.querySelector('.show-all')
    .addEventListener('click', (e) => {
        e.preventDefault();
        const url = e.target.href;
        const bookContainer = document.querySelector('.books-container');
        options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }
        if (bookContainer.classList.contains('unvisible')) {
            fetch(url, options)
            .then(response => response.json())
            .then(data => {
                bookContainer.innerHTML = data.html_favorite;
                e.target.innerHTML = 'Hide all';
                bookContainer.classList.remove('unvisible');
                bookContainer.classList.add('visible');
            });
        } else {
            bookContainer.classList.remove('visible');
            bookContainer.classList.add('unvisible');
            bookContainer.innerHTML = '';
            e.target.innerHTML = 'Show all';
        }
    })
}) ();