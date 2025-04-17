document.addEventListener('DOMContentLoaded', function () {
    const deleteModal = document.getElementById('deleteModal');
    const faqQuestion = document.getElementById('faqQuestion');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

    deleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Button that triggered the modal
        console.log('Modal triggered:', button); // Debugging

        const faqId = button.getAttribute('data-id'); // Get the FAQ ID
        const question = button.getAttribute('data-question'); // Get the FAQ question

        console.log('FAQ ID:', faqId); // Debugging
        console.log('FAQ Question:', question); // Debugging

        // Update the modal content
        faqQuestion.textContent = question;

        // Set the delete link dynamically
        confirmDeleteBtn.href = `/admin-panel/faqs/${faqId}/delete/`; // Replace with your delete URL pattern
    });
});