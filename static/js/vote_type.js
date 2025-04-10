document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function () {
            const faqId = this.dataset.id;
            const voteType = this.dataset.vote;

            fetch(`/faqs/${faqId}/vote/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ vote_type: voteType }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                    } else {
                        const upButton = document.querySelector(`.vote-btn[data-id="${faqId}"][data-vote="up"]`);
                        const downButton = document.querySelector(`.vote-btn[data-id="${faqId}"][data-vote="down"]`);
                        upButton.innerHTML = `👍 ${data.thumbs_up}`;
                        downButton.innerHTML = `👎 ${data.thumbs_down}`;
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });
});

function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}