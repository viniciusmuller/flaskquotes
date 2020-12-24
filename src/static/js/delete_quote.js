let deleteButtons = document.querySelectorAll(".quote-content a");

deleteButtons.forEach((button) => {
  button.addEventListener("click", deleteQuote);
});

async function deleteQuote(event) {
  let quoteID = this.getAttribute("quote-id");

  // Preventing no-href `a` quote tag from doing
  // a DELETE request to the current endpoint
  //event.preventDefault()

  await fetch(`/delete/${quoteID}`, {
    method: "DELETE",
  });

  // Deleting the entire quote div
  this.parentNode.parentNode.remove();
}
