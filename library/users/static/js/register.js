const mySiteUrl = '/library/';

(function () {
    document.querySelector('.js-register-form').addEventListener('submit', function (event) {
        event.preventDefault();
        let formData = new FormData(this);
        options = {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        }
        fetch(this.action, options)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status === 'ok') {
                window.location.replace(mySiteUrl);
            } else {
                throw new Error('Invalid json');
            }
        })
        .catch(err => console.error(err));
    })
}) ();
