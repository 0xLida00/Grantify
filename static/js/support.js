document.addEventListener("DOMContentLoaded", function () {
    console.log("support.js loaded and DOMContentLoaded event triggered.");

    const supportIcon = document.getElementById("support-icon");
    const supportModal = document.getElementById("support-modal");
    const closeModal = document.querySelector(".support-modal .close");
    const supportTicketForm = document.getElementById("support-ticket-form");
    const feedbackForm = document.getElementById("feedback-form");
    const dynamicFlashMessagesContainer = document.querySelector(".dynamic-flash-messages-container");

    // Function to get CSRF token
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    // Function to display flash messages dynamically
    function displayFlashMessage(message, type) {
        const trimmedMessage = message.trim();
    
        const alertDiv = document.createElement("div");
        alertDiv.className = `alert alert-${type} alert-dismissible fade show mt-3`;
        alertDiv.role = "alert";
        alertDiv.innerHTML = `
            ${trimmedMessage}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        if (dynamicFlashMessagesContainer) {
            dynamicFlashMessagesContainer.appendChild(alertDiv);
        } else {
            console.error("Dynamic flash messages container not found in the DOM.");
        }
    
        // Automatically remove the message after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    // Toggle the support modal
    if (supportIcon && supportModal && closeModal) {
        supportIcon.addEventListener("click", function () {
            supportModal.style.display = "block";
        });

        closeModal.addEventListener("click", function () {
            supportModal.style.display = "none";
        });

        window.addEventListener("click", function (e) {
            if (e.target === supportModal) {
                supportModal.style.display = "none";
            }
        });
    }

    // Handle support ticket form submission
    if (supportTicketForm) {
        supportTicketForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const subject = document.getElementById("ticket-subject").value;
            const description = document.getElementById("ticket-description").value;
            const priority = document.getElementById("ticket-priority").value;

            fetch("/api/support-tickets/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ subject, description, priority }),
            })
                .then((response) => response.json().then((data) => ({ status: response.status, body: data })))
                .then(({ status, body }) => {
                    if (status === 201) {
                        displayFlashMessage(body.message, "success");
                        supportTicketForm.reset();
                    } else {
                        displayFlashMessage(body.message, "danger");
                    }
                })
                .catch((error) => {
                    displayFlashMessage("An error occurred. Please try again later.", "danger");
                });
        });
    }

    // Handle feedback form submission
    if (feedbackForm) {
        feedbackForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const message = document.getElementById("feedback-message").value;

            fetch("/api/feedback/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify({ message }),
            })
                .then((response) => response.json().then((data) => ({ status: response.status, body: data })))
                .then(({ status, body }) => {
                    if (status === 201) {
                        displayFlashMessage(body.message, "success");
                        feedbackForm.reset();
                    } else {
                        displayFlashMessage(body.message, "danger");
                    }
                })
                .catch((error) => {
                    displayFlashMessage("An error occurred. Please try again later.", "danger");
                });
        });
    }
});