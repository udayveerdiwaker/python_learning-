// app.js

document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatHistory = document.getElementById("chat-history");
    const typingIndicator = document.getElementById("typing-indicator");
    const connectionBadge = document.getElementById("connection-badge");

    // ------------------------------------------------------------------------------
    // 1. Submit Prompt Handler
    // ------------------------------------------------------------------------------
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        // Clear input field
        chatInput.value = "";

        // Add User Message to Chat UI
        appendMessage(message, "user");

        // Show Typing Indicator & Scroll
        showTypingIndicator(true);
        scrollToBottom();

        try {
            // Send request to API
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error("Failed to communicate with assistant server.");
            }

            const data = await response.json();
            
            // Hide Typing Indicator
            showTypingIndicator(false);

            // Update Badge Mode (Live vs Simulated)
            updateConnectionBadge(data.mode);

            // Add Assistant Message to Chat UI
            appendMessage(data.reply, "assistant");
            scrollToBottom();

        } catch (error) {
            showTypingIndicator(false);
            appendMessage(`⚠️ Error: ${error.message}`, "assistant");
            scrollToBottom();
        }
    });


    // ------------------------------------------------------------------------------
    // 2. DOM Helper Functions
    // ------------------------------------------------------------------------------
    function appendMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", `${sender}-message`);

        const avatarDiv = document.createElement("div");
        avatarDiv.classList.add("avatar");
        avatarDiv.innerHTML = sender === "user" ? 
            '<i class="fa-solid fa-user-ninja"></i>' : 
            '<i class="fa-solid fa-robot"></i>';

        const contentDiv = document.createElement("div");
        contentDiv.classList.add("message-content");
        contentDiv.innerHTML = parseMarkdown(text);

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        chatHistory.appendChild(messageDiv);
    }

    function showTypingIndicator(show) {
        typingIndicator.style.display = show ? "flex" : "none";
        if (show) {
            // Append indicator after the last message block
            chatHistory.appendChild(typingIndicator);
        }
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function updateConnectionBadge(mode) {
        if (mode.includes("Live")) {
            connectionBadge.className = "badge live-mode";
            connectionBadge.innerHTML = '<i class="fa-solid fa-bolt"></i> Live Gemini Active';
        } else {
            connectionBadge.className = "badge local-mode";
            connectionBadge.innerHTML = '<i class="fa-solid fa-server"></i> Local Simulation Mode';
        }
    }


    // ------------------------------------------------------------------------------
    // 3. Simple Markdown Parser
    // ------------------------------------------------------------------------------
    function parseMarkdown(text) {
        // Safe escape HTML characters
        let html = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // Code Blocks ```python ... ```
        html = html.replace(/```([\s\S]+?)```/g, (match, code) => {
            return `<pre><code>${code.trim()}</code></pre>`;
        });

        // Inline Code `code`
        html = html.replace(/`([^`]+)`/g, "<code>$1</code>");

        // Bold text **text**
        html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

        // Headers ### text
        html = html.replace(/^###\s+(.+)$/gm, "<h3>$1</h3>");

        // Split into paragraphs if not inside pre tags
        const lines = html.split("\n\n");
        const parsedParagraphs = lines.map(line => {
            if (line.trim().startsWith("<pre>") || line.trim().startsWith("<h3>")) {
                return line;
            }
            return `<p>${line.replace(/\n/g, "<br>")}</p>`;
        });

        return parsedParagraphs.join("");
    }
});
