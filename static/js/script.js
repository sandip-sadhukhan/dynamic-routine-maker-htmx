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

const clearTooltips = () => {
    const tooltipTriggerList = document.querySelectorAll(
        '[data-bs-toggle="tooltip"]'
    );

    [...tooltipTriggerList].forEach((tooltipTriggerEl) => {
        const tooltip = bootstrap.Tooltip.getOrCreateInstance(tooltipTriggerEl);
        tooltip.dispose();
    });
};

// Close routine modal when the form is submitted
document.body.addEventListener("closeRoutineFormModal", function () {
    const modal = bootstrap.Modal.getInstance("#createRoutineModal");
    modal.hide();
});

// Enable tooltips on page load and whenever htmx makes a request
document.addEventListener("DOMContentLoaded", enableTooltips);
document.body.addEventListener("htmx:afterSettle", enableTooltips);

// Clear tooltip before htmx request, to prevent them from staying on the screen
// even though element may be removed
document.body.addEventListener("htmx:beforeRequest", clearTooltips);
