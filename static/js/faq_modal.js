document.addEventListener("DOMContentLoaded", function () {
    const deleteFaqModal = $("#deleteModal");
    const deleteFaqForm = document.getElementById("deleteFaqForm");

    if (!deleteFaqModal || !deleteFaqForm) {
        console.error("Modal or form not found.");
        return;
    }

    // Handle the modal show event
    deleteFaqModal.on("show.bs.modal", function (event) {
        const button = $(event.relatedTarget);

        if (!button) {
            console.error("No related button found for modal.");
            return;
        }

        const faqUrl = button.data("faq-url");
        const faqQuestion = button.data("faq-question");

        if (!faqUrl) {
            console.error("FAQ URL is missing in button attributes.");
            return;
        }

        deleteFaqForm.setAttribute("action", faqUrl);

        // Update the modal content with the FAQ question
        const faqQuestionElement = document.getElementById("faqQuestion");
        if (faqQuestionElement) {
            faqQuestionElement.textContent = faqQuestion || "No question provided.";
        }
    });
});