const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#chat-messages");
const sendButton = document.querySelector("#send-button");

function addMessage(text, type) {
    const message = document.createElement("div");
    message.className = `message message-${type}`;
    message.textContent = text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");
    input.value = "";
    input.disabled = true;
    sendButton.disabled = true;
    sendButton.textContent = "Sending…";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Request failed.");
        }
        addMessage(data.response, "bot");
    } catch (error) {
        addMessage(error.message || "Unable to reach the chatbot right now.", "bot");
    } finally {
        input.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = "Send";
        input.focus();
    }
});
