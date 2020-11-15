
let postQuoteForm = document.querySelector("#quote-form");
postQuoteForm.addEventListener("submit", postQuote);

let quotesDiv = document.querySelector(".quotes");
let flashDiv = document.querySelector(".flashdiv");


async function postQuote(event) {

    event.preventDefault();

    let inputElement = this.elements[1];

    // Do not submit to server if the input is empty
    if(!inputElement.value) return;

    // Parsing form data to insert it into request body 
    let data = new URLSearchParams(new FormData(this));

    let response = await fetch("/post", {
        body: data,
        method: "POST"
    });
    let responseJSON = await response.json();

    if(responseJSON["success"]) {
        createQuote(responseJSON);
        // Cleaning input value
        inputElement.value = '';
    }
    else {
        // TODO use another way to alert
        // the user instead of alert
        alert(responseJSON["reason"]);
    }
}


function createQuote({timestamp, content, id}) {

    // Creating the main quote div
    let mainQuoteElement = document.createElement("div");
    mainQuoteElement.classList.add("user-quote");

    // Creating the inner quote elements
    let quote = document.createElement("div");
    quote.classList.add("quote-content");
    mainQuoteElement.append(quote);

    // Creating the quote content element
    let quoteText = document.createElement('q');
    quoteText.innerHTML = content;
    quote.append(quoteText);

    // Creating the timestamp element
    let timestampElement = document.createElement('p');
    timestampElement.innerHTML = timestamp;
    quote.append(timestampElement);

    // Creating the quote delete button
    let deleteButton = document.createElement('a');
    deleteButton.innerHTML = "Delete";
    deleteButton.setAttribute("quote-id", id);
    deleteButton.classList.add("delete-quote-btn");
    deleteButton.addEventListener("click", deleteQuote)
    quote.append(deleteButton);

    // Appending the finished quote as 
    // the first child of the quotes div
    quotesDiv.prepend(mainQuoteElement);
}
