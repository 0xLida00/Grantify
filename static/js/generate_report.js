document.addEventListener('DOMContentLoaded', function () {
    const generateReportBtn = document.getElementById('generateReportBtn');

    if (generateReportBtn) {
        generateReportBtn.addEventListener('click', function () {
            fetch('/reports/generate/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(data.message);
                        location.reload();
                    }
                })
                .catch(error => console.error('Error generating report:', error));
        });
    }

    // Helper function to get CSRF token
    function getCSRFToken() {
        const csrfToken = document.getElementById('csrfToken');
        return csrfToken ? csrfToken.value : '';
    }
});