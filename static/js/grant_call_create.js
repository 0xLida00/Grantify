    document.addEventListener("DOMContentLoaded", function () {
        // Add Question Button
        document.getElementById("add-question").addEventListener("click", function () {
            const container = document.getElementById("questions-container");
            const totalForms = document.querySelector("#id_questions-TOTAL_FORMS");
            const formCount = parseInt(totalForms.value, 10);

            // Clone the last question form
            const newForm = container.lastElementChild.cloneNode(true);
            newForm.querySelectorAll("input, select, textarea").forEach(function (input) {
                const name = input.name.replace(`-${formCount - 1}-`, `-${formCount}-`);
                const id = input.id.replace(`-${formCount - 1}-`, `-${formCount}-`);
                input.name = name;
                input.id = id;
                input.value = ""; // Clear the value
            });

            container.appendChild(newForm);
            totalForms.value = formCount + 1; // Increment the total forms count
        });
    });