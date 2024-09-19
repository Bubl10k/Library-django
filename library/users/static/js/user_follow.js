(function () {
    document.querySelectorAll('.follow-button').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            let action = button.dataset.action;
            const userId = button.dataset.userId;
            const options = {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
            }
            let formData = new FormData();
            formData.append('id', userId);
            formData.append('action', action);
            options['body'] = formData;
            console.log(action);

            fetch(button.href, options)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    let newAction = 'Unfollow' === action ? 'Follow' : 'Unfollow';
                    button.dataset.action = newAction;
                    button.innerHTML = newAction;
                    let followersCount = document.querySelector('.follower-count-' + userId);
                    let totalCount = parseInt(followersCount.innerHTML);
                    followersCount.innerHTML = action === 'Unfollow' ? totalCount - 1 : totalCount + 1;
                }
            })
        })
    })
}) ();