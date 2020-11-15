// Prevent "Confirm Form Resubmission" dialog boxes
if(window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
