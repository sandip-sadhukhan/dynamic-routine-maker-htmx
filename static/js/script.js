// Enable bootstrap tooltips
const enableTooltips = function () {
    console.log("called");
    const tooltipTriggerList = document.querySelectorAll(
        '[data-bs-toggle="tooltip"]'
    );

    [...tooltipTriggerList].forEach((tooltipTriggerEl) =>
        bootstrap.Tooltip.getOrCreateInstance(tooltipTriggerEl)
    );
};

// Close routine modal when the form is submitted
document.body.addEventListener("closeRoutineFormModal", function () {
    const modal = bootstrap.Modal.getInstance("#createRoutineModal");
    modal.hide();
});

// Enable tooltips on page load and whenever htmx makes a request
document.addEventListener("DOMContentLoaded", enableTooltips);
document.body.addEventListener("htmx:afterSettle", enableTooltips);
