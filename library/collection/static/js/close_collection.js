(function () {
    document.querySelector('.js-close-collection')
    .addEventListener('click', () => {
        document.querySelector('.container').innerHTML = '';
    });
})();