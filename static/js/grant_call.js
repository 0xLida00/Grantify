document.addEventListener("DOMContentLoaded", function () {
    const deleteGrantCallModal = $("#deleteModal");
    const deleteGrantCallForm = document.getElementById("deleteGrantCallForm");

    if (!deleteGrantCallModal || !deleteGrantCallForm) {
        console.error("Modal or form not found.");
        return;
    }

    // Handle the modal show event
    deleteGrantCallModal.on("show.bs.modal", function (event) {
        const button = $(event.relatedTarget); // Button that triggered the modal

        if (!button) {
            console.error("No related button found for modal.");
            return;
        }

        const grantCallUrl = button.data("grant-call-url"); // Get the URL from data attribute

        if (!grantCallUrl) {
            console.error("Grant Call URL is missing in button attributes.");
            return;
        }

        // Set the form action to the grant call's delete URL
        deleteGrantCallForm.setAttribute("action", grantCallUrl);
    });
});