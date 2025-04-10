document.addEventListener('DOMContentLoaded', function () {
    const choiceWrappers = document.querySelectorAll('.choices-wrapper');

    choiceWrappers.forEach(wrapper => {
        const checkboxes = wrapper.querySelectorAll('input.form-check-input');
        const labels = wrapper.querySelectorAll('label.form-check-label');

        checkboxes.forEach(input => {
            input.style.marginLeft = '15px';
            input.style.marginRight = '10px';
        });

        labels.forEach(label => {
            label.style.marginLeft = '5px';
            label.style.whiteSpace = 'nowrap';
        });
    });
});