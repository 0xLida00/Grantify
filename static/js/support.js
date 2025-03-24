document.addEventListener("DOMContentLoaded", function () {
    const supportIcon = document.getElementById("support-icon");
    const supportModal = document.getElementById("support-modal");
    const closeModal = document.querySelector(".support-modal .close");
    const faqList = document.getElementById("faq-list");
    const supportTicketForm = document.getElementById("support-ticket-form");
    const feedbackForm = document.getElementById("feedback-form");

    // Function to get CSRF token
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    // Ensure elements exist before adding event listeners
    if (supportIcon && supportModal && closeModal) {
        // Toggle the support modal
        supportIcon.addEventListener("click", function () {
            supportModal.style.display = "block";
        });

        closeModal.addEventListener("click", function () {
            supportModal.style.display = "none";
        });

        // Close modal when clicking outside of it
        window.addEventListener("click", function (e) {
            if (e.target === supportModal) {
                supportModal.style.display = "none";
            }
        });
    }

    // Fetch FAQs
    if (faqList) {
        fetch("/api/faqs/")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch FAQs");
                }
                return response.json();
            })
            .then((data) => {
                faqList.innerHTML = "";
                data.forEach((faq) => {
                    const li = document.createElement("li");
                    li.innerHTML = `<strong>${faq.question}</strong><p>${faq.answer}</p>`;
                    faqList.appendChild(li);
                });
            })
            .catch((error) => console.error("Error fetching FAQs:", error));
    }

    // Handle support ticket form submission
    if (supportTicketForm) {
        supportTicketForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const subject = document.getElementById("ticket-subject").value;
            const description = document.getElementById("ticket-description").value;

            fetch("/api/support-tickets/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(), // Add CSRF token
                },
                body: JSON.stringify({ subject, description }),
            })
                .then((response) => {
                    if (response.ok) {
                        alert("Support ticket created successfully!");
                        supportTicketForm.reset();
                    } else {
                        alert("Failed to create support ticket.");
                    }
                })
                .catch((error) => console.error("Error creating support ticket:", error));
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
                    "X-CSRFToken": getCSRFToken(), // Add CSRF token
                },
                body: JSON.stringify({ message }),
            })
                .then((response) => {
                    if (response.ok) {
                        alert("Feedback submitted successfully!");
                        feedbackForm.reset();
                    } else {
                        alert("Failed to submit feedback.");
                    }
                })
                .catch((error) => console.error("Error submitting feedback:", error));
        });
    }
});