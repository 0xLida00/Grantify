document.addEventListener("DOMContentLoaded", function () {
    const supportIcon = document.getElementById("support-icon");
    const supportModal = document.getElementById("support-modal");
    const closeModal = document.querySelector(".support-modal .close");
    const supportTicketForm = document.getElementById("support-ticket-form");
    const feedbackForm = document.getElementById("feedback-form");
    const dynamicFlashMessagesContainer = document.querySelector(".dynamic-flash-messages-container");

    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    // Function to display flash messages dynamically
    function displayFlashMessage(message, type) {
        if (!message) {
            console.error("No message provided for flash message.");
            return;
        }

        const trimmedMessage = message.trim();
        const alertDiv = document.createElement("div");
        alertDiv.className = `alert alert-${type} fade show mt-3`;
        alertDiv.role = "alert";
        alertDiv.innerHTML = `
            <span>${trimmedMessage}</span>
        `;

        if (dynamicFlashMessagesContainer) {
            dynamicFlashMessagesContainer.appendChild(alertDiv);
        } else {
            console.error("Dynamic flash messages container not found in the DOM.");
        }

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
            const subject = document.getElementById("ticket-subject").value.trim();
            const description = document.getElementById("ticket-description").value.trim();
            const priority = document.getElementById("ticket-priority").value;

            if (!subject || !description || !priority) {
                displayFlashMessage("All fields are required to submit a support ticket.", "danger");
                return;
            }

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
                        displayFlashMessage(body.message || "Support ticket created successfully!", "success");
                        supportTicketForm.reset();
                    } else if (status === 401) {
                        displayFlashMessage("You must be logged in to submit a support ticket.", "danger");
                    } else {
                        const errorMessage = body.message || "Failed to submit the support ticket.";
                        displayFlashMessage(errorMessage, "danger");
                    }
                })
                .catch((error) => {
                    console.error("Error submitting support ticket:", error);
                    displayFlashMessage("An error occurred. Please try again later.", "danger");
                });
        });
    }

    // Handle feedback form submission
    if (feedbackForm) {
        feedbackForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const message = document.getElementById("feedback-message").value.trim();

            if (!message) {
                displayFlashMessage("Feedback message cannot be empty.", "danger");
                return;
            }

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
                        displayFlashMessage(body.message || "Feedback submitted successfully!", "success");
                        feedbackForm.reset();
                    } else if (status === 401) {
                        displayFlashMessage("You must be logged in to submit feedback.", "danger");
                    } else {
                        const errorMessage = body.message || "Failed to submit feedback.";
                        displayFlashMessage(errorMessage, "danger");
                    }
                })
                .catch((error) => {
                    console.error("Error submitting feedback:", error);
                    displayFlashMessage("An error occurred. Please try again later.", "danger");
                });
        });
    }
});