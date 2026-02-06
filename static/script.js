/**
 * Chat Application JavaScript
 * Handles UI interactions and API communication
 */

// Global state
let isConnected = false;
let isLoading = false;
let conversationHistory = []; // Mantener histórico completo

// DOM Elements
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const messagesList = document.getElementById("messages");
const chatForm = document.getElementById("chat-form");
const statusIndicator = document.getElementById("status-indicator");
const statusText = document.getElementById("status-text");

// Initialize the application
document.addEventListener("DOMContentLoaded", async () => {
    await checkConnection();
    setupEventListeners();
    focusInput();
});

/**
 * Setup event listeners for the application
 */
function setupEventListeners() {
    chatForm.addEventListener("submit", handleSubmit);
    messageInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    });
}

/**
 * Check connection to the backend
 */
async function checkConnection() {
    try {
        const response = await fetch("/health", {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        if (response.ok) {
            const data = await response.json();
            if (data.agent_ready) {
                setConnected(true);
            } else {
                setConnected(false, "Agente não está pronto - configure as credenciais");
            }
        } else {
            setConnected(false, "Servidor indisponível");
        }
    } catch (error) {
        console.error("Connection check failed:", error);
        setConnected(false, "Conexão recusada");
    }
}

/**
 * Set connection status
 */
function setConnected(connected, reason = null) {
    isConnected = connected;

    if (connected) {
        statusIndicator.classList.add("connected");
        statusIndicator.classList.remove("disconnected");
        statusText.textContent = "Conectado";
        messageInput.disabled = false;
        sendButton.disabled = false;
    } else {
        statusIndicator.classList.add("disconnected");
        statusIndicator.classList.remove("connected");
        statusText.textContent = reason || "Desconectado";
        messageInput.disabled = true;
        sendButton.disabled = true;
    }
}

/**
 * Handle form submission
 */
async function handleSubmit(event) {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) return;
    if (!isConnected || isLoading) return;

    // Clear input
    messageInput.value = "";
    messageInput.focus();

    // Add user message to UI
    addMessage(message, "user");

    // Set loading state
    isLoading = true;
    sendButton.disabled = true;

    // Show loading indicator
    const loadingMessageId = addLoadingMessage();

    try {
        // Agregar mensaje al histórico
        conversationHistory.push({ role: "user", content: message });
        
        // Enviar con el histórico completo
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                content: message, 
                role: "user",
                history: conversationHistory
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Erro desconhecido");
        }

        const data = await response.json();

        if (data.success && data.message) {
            // Remove loading message
            removeMessage(loadingMessageId);
            // Add assistant response
            addMessage(data.message, "assistant");
            // Agregar respuesta al histórico
            conversationHistory.push({ role: "assistant", content: data.message });
        } else {
            removeMessage(loadingMessageId);
            addMessage(
                data.error || "Erro ao processar a mensagem",
                "assistant",
                true
            );
        }
    } catch (error) {
        console.error("Error:", error);
        removeMessage(loadingMessageId);
        
        let errorMsg = error.message;
        if (error.message.includes("API Error 400")) {
            errorMsg += "\n\n💡 Dica: Verifique se as credenciais do Azure Foundry estão corretas no arquivo .env";
        }
        
        addMessage(
            `❌ Erro: ${errorMsg}. Verifique a conexão e o arquivo .env.`,
            "assistant",
            true
        );
    } finally {
        isLoading = false;
        sendButton.disabled = !isConnected;
        messageInput.focus();
    }
}

/**
 * Add a message to the chat
 */
function addMessage(content, role, isError = false) {
    // Remove welcome message if it exists
    const welcomeMsg = messagesList.querySelector(".welcome-message");
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", role);

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");
    if (isError) {
        contentDiv.classList.add("error-message");
    }

    // Format text with basic markdown support
    contentDiv.innerHTML = formatText(content);

    messageDiv.appendChild(contentDiv);
    messagesList.appendChild(messageDiv);

    // Scroll to bottom
    scrollToBottom();

    return messageDiv;
}

/**
 * Add a loading message
 */
function addLoadingMessage() {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "assistant", "loading");
    messageDiv.id = "loading-message";

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");

    contentDiv.innerHTML = `
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
    `;

    messageDiv.appendChild(contentDiv);
    messagesList.appendChild(messageDiv);

    scrollToBottom();

    return messageDiv.id;
}

/**
 * Remove a message by ID
 */
function removeMessage(messageId) {
    const messageElement = document.getElementById(messageId);
    if (messageElement) {
        messageElement.remove();
    }
}

/**
 * Format text content with basic markdown support
 */
function formatText(text) {
    // Escape HTML
    let formatted = escapeHtml(text);

    // Basic markdown formatting
    // Bold: **text** -> <strong>text</strong>
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    // Italic: *text* -> <em>text</em>
    formatted = formatted.replace(/\*(.*?)\*/g, "<em>$1</em>");

    // Line breaks
    formatted = formatted.replace(/\n/g, "<br>");

    // Code blocks: `code` -> <code>code</code>
    formatted = formatted.replace(/`(.*?)`/g, "<code>$1</code>");

    return formatted;
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    messagesList.scrollTop = messagesList.scrollHeight;
}

/**
 * Focus on message input
 */
function focusInput() {
    if (isConnected) {
        messageInput.focus();
    }
}

/**
 * Send a predefined message (for suggestions)
 */
function sendMessage(text) {
    messageInput.value = text;
    handleSubmit(new Event("submit"));
}

/**
 * Clear chat history
 */
function clearChat() {
    messagesList.innerHTML = `
        <div class="welcome-message">
            <h2>👋 Bem-vindo!</h2>
            <p>Comece fazendo uma pergunta ao avaliador de AI-102</p>
        </div>
    `;
    conversationHistory = []; // Limpar histórico
    messageInput.value = "";
    focusInput();
}
