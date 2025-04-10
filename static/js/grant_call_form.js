document.addEventListener("DOMContentLoaded", function () {
    const addQuestionButton = document.getElementById("add-question");
    const questionsContainer = document.getElementById("questions-container");
    const totalForms = document.querySelector("#id_questions-TOTAL_FORMS");
    const saveButton = document.querySelector("button[type='submit']");

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

            questionTypeField.dispatchEvent(new Event("change"));
        }
    }

    questionsContainer.querySelectorAll(".question-form").forEach(function (questionForm) {
        toggleChoicesSection(questionForm);
    });

    // Function to add a new question form
    addQuestionButton.addEventListener("click", function () {
        const formCount = parseInt(totalForms.value, 10);

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

            if (!input.name.endsWith("-id")) {
                input.value = "";
            }
        });

        questionsContainer.appendChild(newForm);
        totalForms.value = formCount + 1;

        toggleChoicesSection(newForm);
    });

    if (saveButton) {
        saveButton.addEventListener("click", function (event) {
            const form = saveButton.closest("form");
            if (form) {
                console.log("Form is being submitted...");
            } else {
                console.error("Form not found!");
            }
        });
    }

    // Function to highlight invalid fields dynamically
    function highlightInvalidFields() {
        document.querySelectorAll(".invalid-feedback").forEach(function (errorElement) {
            const input = errorElement.previousElementSibling;
            if (input) {
                input.classList.add("is-invalid");
            }
        });
    }

    highlightInvalidFields();

    document.querySelector("form").addEventListener("submit", function (event) {
        setTimeout(highlightInvalidFields, 100);
    });
});