const Chat = {
    messagesContainer: null,

    init() {
        this.messagesContainer = document.getElementById("messages");
    },

    addMessage(role, content) {
        const welcome = this.messagesContainer.querySelector(".welcome-message");
        if (welcome) welcome.remove();

        const message = document.createElement("div");
        message.classList.add("message", role);

        const avatar = document.createElement("div");
        avatar.classList.add("avatar");
        avatar.textContent = role === "user" ? "👤" : "🧠";

        const bubble = document.createElement("div");
        bubble.classList.add("bubble");
        bubble.textContent = content;

        message.appendChild(avatar);
        message.appendChild(bubble);
        this.messagesContainer.appendChild(message);
        this.scrollToBottom();
    },

    addStreamingMessage() {
        const welcome = this.messagesContainer.querySelector(".welcome-message");
        if (welcome) welcome.remove();

        const message = document.createElement("div");
        message.classList.add("message", "assistant");

        const avatar = document.createElement("div");
        avatar.classList.add("avatar");
        avatar.textContent = "🧠";

        const bubble = document.createElement("div");
        bubble.classList.add("bubble");
        bubble.id = "streaming-bubble";
        bubble.textContent = "";

        message.appendChild(avatar);
        message.appendChild(bubble);
        this.messagesContainer.appendChild(message);
        return bubble;
    },

    appendChunk(bubble, chunk) {
        bubble.textContent += chunk;
        this.scrollToBottom();
    },

    showTyping() {
        const message = document.createElement("div");
        message.classList.add("message", "assistant");
        message.id = "typing-indicator";

        const avatar = document.createElement("div");
        avatar.classList.add("avatar");
        avatar.textContent = "🧠";

        const bubble = document.createElement("div");
        bubble.classList.add("bubble");
        bubble.innerHTML = `
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        `;

        message.appendChild(avatar);
        message.appendChild(bubble);
        this.messagesContainer.appendChild(message);
        this.scrollToBottom();
    },

    hideTyping() {
        const indicator = document.getElementById("typing-indicator");
        if (indicator) indicator.remove();
    },

    updateAgentBadge(agentName) {
        const badge = document.getElementById("agent-badge");
        const icons = { "Researcher": "🔍", "Summarizer": "📝", "FactChecker": "✅" };
        const icon = icons[agentName] || "🤖";
        badge.textContent = `${icon} ${agentName}`;
    },

    clear() {
        this.messagesContainer.innerHTML = `
            <div class="welcome-message">
                <h2>Welcome to OmniMind 🧠</h2>
                <p>Ask me anything or upload a document to get started.</p>
            </div>
        `;
    },

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
};