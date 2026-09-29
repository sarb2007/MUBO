const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const chat = document.getElementById("chat");


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const message = input.value.trim();

    if (!message) {
        return;
    }

    // Show the user's message immediately.
    addMessage(message, "user");

    input.value = "";

    // For now, we are just testing the connection.
    const response = await fetch("/api/chat", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    addMessage(data.response, "ai");
});


function addMessage(text, sender) {

    const message = document.createElement("div");

    message.className = `message ${sender}`;

    message.textContent = text;

    chat.appendChild(message);

    // Keep the newest message visible.
    chat.scrollTop = chat.scrollHeight;
}