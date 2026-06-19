const API_BASE = "http://localhost:8000";

const API = {
    async chat(message) {
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });
        if (!response.ok) throw new Error("Chat request failed");
        return await response.json();
    },

    async streamChat(message, onChunk, onAgentDetected, onDone) {
        const response = await fetch(`${API_BASE}/chat/stream`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const text = decoder.decode(value);
            const lines = text.split("\n");

            for (const line of lines) {
                if (line.startsWith("data: ")) {
                    const data = JSON.parse(line.slice(6));
                    if (data.type === "agent") onAgentDetected(data.agent);
                    else if (data.type === "chunk") onChunk(data.content);
                    else if (data.type === "done") onDone();
                }
            }
        }
    },

    async uploadDocument(file) {
        const formData = new FormData();
        formData.append("file", file);
        const response = await fetch(`${API_BASE}/upload`, {
            method: "POST",
            body: formData
        });
        if (!response.ok) throw new Error("Upload failed");
        return await response.json();
    },

    async getHistory() {
        const response = await fetch(`${API_BASE}/history`);
        if (!response.ok) throw new Error("Failed to get history");
        return await response.json();
    },

    async clearHistory() {
        const response = await fetch(`${API_BASE}/history`, { method: "DELETE" });
        if (!response.ok) throw new Error("Failed to clear history");
        return await response.json();
    },

    async healthCheck() {
        const response = await fetch(`${API_BASE}/health`);
        if (!response.ok) throw new Error("Health check failed");
        return await response.json();
    }
};