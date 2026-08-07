const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

form.addEventListener("submit", async function(event) {
    // Prevent the form from submitting normally
    event.preventDefault(); 

    const message = input.value.trim();
    if (message === "") return; // Don't send empty messages

    chatBox.innerHTML += `
        <p><strong>You:</strong> ${message}</p>
    `;

    input.value = "";

    const response = await fetch("/halo", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    });
    // Get the JSON response from the server
    const data = await response.json();
    chatBox.innerHTML += `
        <p><strong>HALO:</strong> ${data.answer}</p>
    `;
});