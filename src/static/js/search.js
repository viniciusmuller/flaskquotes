let searchForm = document.querySelector("#search-form");
let userInput = document.querySelector("#search-bar");

searchForm.addEventListener("submit", (event) => {
  // Preventing form from submit
  event.preventDefault();
  // Redirecting user to searched profile
  window.location.href = `/user/${userInput.value}`;
});
