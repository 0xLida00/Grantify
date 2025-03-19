document.addEventListener("DOMContentLoaded", function () {
    const addQuestionButton = document.getElementById("add-question");
    const questionsContainer = document.getElementById("questions-container");
    const totalForms = document.querySelector("#id_form-TOTAL_FORMS");

    if (!addQuestionButton || !questionsContainer || !totalForms) {
        console.error("Required elements for adding questions are missing.");
        return;
    }

    addQuestionButton.addEventListener("click", function () {
        const newFormIndex = totalForms.value;
        const emptyFormTemplate = document.querySelector(".question-form").outerHTML;

        if (!emptyFormTemplate) {
            console.error("Empty form template not found.");
            return;
        }

        const newFormHtml = emptyFormTemplate.replace(/-0-/g, `-${newFormIndex}-`);
        questionsContainer.insertAdjacentHTML("beforeend", newFormHtml);
        totalForms.value = parseInt(totalForms.value) + 1;
    });
});