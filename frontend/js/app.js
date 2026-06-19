document.addEventListener("DOMContentLoaded", () => {
    Chat.init();

    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const newChatBtn = document.getElementById("new-chat-btn");
    const fileInput = document.getElementById("file-input");
    const uploadStatus = document.getElementById("upload-status");

    userInput.addEventListener("input", () => {
        userInput.style.height = "auto";
        userInput.style.height = userInput.scrollHeight + "px";
    });

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener("click", sendMessage);

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        userInput.value = "";
        userInput.style.height = "auto";
        sendBtn.disabled = true;

        Chat.addMessage("user", message);
        Chat.showTyping();

        let bubble = null;

        const response = await fetch(`http://localhost:8000/chat/stream`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const text = decoder.decode(value);
                const lines = text.split("\n");

                for (const line of lines) {
                    if (!line.startsWith("data: ")) continue;

                    const data = JSON.parse(line.slice(6));

                    if (data.type === "agent") {
                        Chat.updateAgentBadge(data.agent);
                    }
                    else if (data.type === "chunk") {
                        if (!bubble) {
                            Chat.hideTyping();
                            bubble = Chat.addStreamingMessage();
                        }
                        Chat.appendChunk(bubble, data.content);
                    }
                    else if (data.type === "done") {
                        if (bubble) bubble.removeAttribute("id");
                    }
                }
            }
        } catch (error) {
            Chat.hideTyping();
            Chat.addMessage("assistant", "❌ Something went wrong. Please try again.");
            console.error(error);
        } finally {
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    newChatBtn.addEventListener("click", async () => {
        try {
            await API.clearHistory();
            Chat.clear();
        } catch (error) {
            console.error("Failed to clear history:", error);
        }
    });

    fileInput.addEventListener("change", async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        uploadStatus.textContent = "Uploading...";

        try {
            const data = await API.uploadDocument(file);
            uploadStatus.textContent = `✅ ${data.filename} uploaded!`;
        } catch (error) {
            uploadStatus.textContent = "❌ Upload failed.";
            console.error(error);
        }

        fileInput.value = "";
    });
});