document.addEventListener("DOMContentLoaded", function () {
    const chatbotIcon = document.getElementById("chatbot-icon");
    const chatbotModal = document.getElementById("chatbot-modal");
    const closeModal = document.querySelector(".chatbot-modal .close");
    const messagesDiv = document.getElementById("messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    let isRequestInProgress = false; // Prevent spamming requests

    // Open the chatbot modal
    chatbotIcon.addEventListener("click", function () {
        chatbotModal.style.display = "block";
    });

    // Close the chatbot modal
    closeModal.addEventListener("click", function () {
        chatbotModal.style.display = "none";
    });

    // Function to send a message to the chatbot
    function sendMessageToChatbot(userMessage) {
        if (isRequestInProgress) {
            alert("Please wait before sending another message.");
            return;
        }

        // Display user message
        const userMessageDiv = document.createElement("div");
        userMessageDiv.textContent = `You: ${userMessage}`;
        userMessageDiv.className = "user-message";
        messagesDiv.appendChild(userMessageDiv);

        // Clear input
        userInput.value = "";

        // Set request in progress
        isRequestInProgress = true;

        // Send message to the backend
        fetch("/support/api/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userMessage }),
        })
            .then((response) => {
                if (response.status === 429) {
                    // Handle rate limit error
                    alert("Rate limit exceeded. Retrying in 5 seconds...");
                    setTimeout(() => sendMessageToChatbot(userMessage), 5000); // Retry after 5 seconds
                    return null;
                }
                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                if (data && data.message) {
                    // Display chatbot response
                    const botMessageDiv = document.createElement("div");
                    botMessageDiv.textContent = `Bot: ${data.message}`;
                    botMessageDiv.className = "bot-message";
                    messagesDiv.appendChild(botMessageDiv);

                    // Scroll to the bottom
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                const errorMessageDiv = document.createElement("div");
                errorMessageDiv.textContent = "Bot: Sorry, something went wrong. Please try again later.";
                errorMessageDiv.className = "bot-message error";
                messagesDiv.appendChild(errorMessageDiv);
            })
            .finally(() => {
                // Allow new requests after 2 seconds
                setTimeout(() => {
                    isRequestInProgress = false;
                }, 2000);
            });
    }

    // Handle send button click
    sendButton.addEventListener("click", function () {
        const userMessage = userInput.value.trim();
        if (!userMessage) {
            alert("Please enter a message.");
            return;
        }
        sendMessageToChatbot(userMessage);
    });

    // Handle Enter key press
    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            const userMessage = userInput.value.trim();
            if (!userMessage) {
                alert("Please enter a message.");
                return;
            }
            sendMessageToChatbot(userMessage);
        }
    });
});