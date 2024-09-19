(function() {
    document.querySelectorAll('.fav-button')
    .forEach(btn => {
        btn.addEventListener('click',
            () => {
                const url = btn.dataset.bookUrl;
                let action = btn.dataset.action;

                const options = {
                        method: 'POST',
                        headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                }
                let formData = new FormData();
                formData.append('action', action);
                options['body'] = formData;
                fetch(url, options)
                .then(response => response.json())
                .then(data => {
                    if (data.status) {
                        console.log(action);
                        let newAction = 'unfavorite' === action ? 'favorite' : 'unfavorite';
                        btn.dataset.action = newAction;
                        let newInnerHtml = btn.innerHTML.replace(action === 'unfavorite' ? 'Delete from favorite' : 'Add to favorite', 
                            newAction === 'unfavorite' ? 'Delete from favorite' : 'Add to favorite');
                        btn.innerHTML = newInnerHtml;
                    }
                })
            } 
        )
    })
}) ();