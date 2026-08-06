const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", function(event) {
    // Prevent the form from submitting normally
    event.preventDefault(); 

    const message = input.value;

    console.log(message);
});