document.addEventListener('DOMContentLoaded', function() {
    document.body.querySelectorAll('.js-change-status').forEach(button => {
        button.addEventListener('click', function() {
            let bookStatus = this.dataset.bookStatus;
            const newStatus = bookStatus == 'U' ? 'R' : 'U';
            this.dataset.bookStatus = newStatus;
            let statusContainer = this.previousElementSibling;
            if (newStatus === 'R') {
                statusContainer.innerHTML = 'Read';
                statusContainer.classList.remove('Unread');
                statusContainer.classList.add('Read');
            } else {
                statusContainer.innerHTML = 'Unread';
                statusContainer.classList.remove('Read');
                statusContainer.classList.add('Unread');
            }
            let options = {
                method: 'POST',
                body: JSON.stringify({status: newStatus}),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
            }
            
            fetch(this.dataset.url, options)
            .then(response => response.json())
            .then(data => {
                if (data.status) {
                    console.log('Confirm');
                } else {
                    console.error('Error');
                }
            })
        });
    })
});

