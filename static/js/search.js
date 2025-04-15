document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                const query = e.target.value.trim();
                if (query) {

                    window.location.href = searchInput.dataset.searchUrl + '?q=' + encodeURIComponent(query);
                }
            }
        });
    }
});