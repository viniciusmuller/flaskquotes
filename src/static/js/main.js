document.addEventListener('DOMContentLoaded', () => {
    //prevent "Confirm Form Resubmission" dialog boxes
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }

    //search-bar
    const searchForm = document.querySelector('#search-form');
    const userInput = document.querySelector('#search-bar');
    searchForm.addEventListener('submit', () => {
        event.preventDefault();
        window.location.href = `/user/${userInput.value}`;
    });
});