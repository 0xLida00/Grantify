document.addEventListener("DOMContentLoaded", function () {
    const addQuestionButton = document.getElementById("add-question");
    const questionsContainer = document.getElementById("questions-container");
    const totalForms = document.querySelector("#id_questions-TOTAL_FORMS");

    if (!addQuestionButton || !questionsContainer || !totalForms) {
        console.error("Required elements for adding questions are missing.");
        return;
    }

    // Function to toggle the visibility of the choices section
    function toggleChoicesSection(questionForm) {
        const questionTypeField = questionForm.querySelector("[name$='-question_type']");
        const choicesSection = questionForm.querySelector(".choices-section");

        if (questionTypeField && choicesSection) {
            questionTypeField.addEventListener("change", function () {
                if (this.value === "multiple_choice") {
                    choicesSection.style.display = "block";
                } else {
                    choicesSection.style.display = "none";
                }
            });

            // Trigger the change event on page load to set the initial state
            questionTypeField.dispatchEvent(new Event("change"));
        }
    }

    // Apply toggleChoicesSection to all existing question forms
    questionsContainer.querySelectorAll(".question-form").forEach(function (questionForm) {
        toggleChoicesSection(questionForm);
    });

    // Function to add a new question form
    addQuestionButton.addEventListener("click", function () {
        const formCount = parseInt(totalForms.value, 10);

        // Clone the last question form
        const lastForm = questionsContainer.lastElementChild;
        if (!lastForm) {
            console.error("No question form template found to clone.");
            return;
        }

        const newForm = lastForm.cloneNode(true);
        newForm.querySelectorAll("input, select, textarea").forEach(function (input) {
            const name = input.name.replace(`-${formCount - 1}-`, `-${formCount}-`);
            const id = input.id.replace(`-${formCount - 1}-`, `-${formCount}-`);
            input.name = name;
            input.id = id;

            // Clear the value for new fields, but do not clear the hidden ID field
            if (!input.name.endsWith("-id")) {
                input.value = "";
            }
        });

        questionsContainer.appendChild(newForm);
        totalForms.value = formCount + 1;

        // Apply toggleChoicesSection to the new question form
        toggleChoicesSection(newForm);
    });
});