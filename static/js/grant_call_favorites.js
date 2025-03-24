document.addEventListener("DOMContentLoaded", function () {
    const favoriteButtons = document.querySelectorAll(".favorite-toggle");

    favoriteButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const grantId = this.getAttribute("data-grant-id");
            const icon = this.querySelector("i");
            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            fetch(`/calls/${grantId}/toggle-favorite/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.is_favorited) {
                        icon.classList.remove("far", "text-muted");
                        icon.classList.add("fas", "text-danger");
                    } else {
                        icon.classList.remove("fas", "text-danger");
                        icon.classList.add("far", "text-muted");
                    }
                })
                .catch((error) => console.error("Error:", error));
        });
    });
});