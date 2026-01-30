/**
 * Watch Insurance Advisor - Chat Client
 * Handles all chat interactions with Netlify Functions backend
 */

// State
let isLoading = false;
let conversationHistory = []; // Store conversation history client-side

// API endpoint for Netlify Functions
const API_ENDPOINT = '/.netlify/functions/chat';

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const welcomeCard = document.getElementById('welcomeCard');
const inputArea = document.getElementById('inputArea');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

/**
 * Start the chat conversation
 */
async function startChat() {
    // Hide welcome card
    welcomeCard.style.display = 'none';
    
    // Show input area
    inputArea.style.display = 'block';
    
    // Reset conversation history
    conversationHistory = [];
    
    // Show loading indicator
    showLoading();
    
    // Get initial greeting from the AI (empty messages array triggers opening)
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ messages: [] })
        });
        
        const data = await response.json();
        
        // Remove loading
        hideLoading();
        
        // Add to conversation history
        conversationHistory.push({ role: 'assistant', content: data.response });
        
        // Add assistant message to UI
        addMessage('assistant', data.response);
        
        // Focus input
        messageInput.focus();
    } catch (error) {
        hideLoading();
        addMessage('assistant', 'I apologize, but I\'m having trouble connecting. Please refresh and try again.');
    }
}

/**
 * Send a message to the chat
 */
async function sendMessage(event) {
    event.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isLoading) return;
    
    // Clear input
    messageInput.value = '';
    
    // Add user message to UI
    addMessage('user', message);
    
    // Add to conversation history
    conversationHistory.push({ role: 'user', content: message });
    
    // Show loading
    showLoading();
    
    // Disable send button
    sendBtn.disabled = true;
    
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ messages: conversationHistory })
        });
        
        const data = await response.json();
        
        // Remove loading
        hideLoading();
        
        // Add to conversation history
        conversationHistory.push({ role: 'assistant', content: data.response });
        
        // Add assistant message to UI
        addMessage('assistant', data.response);
        
    } catch (error) {
        hideLoading();
        addMessage('assistant', 'I apologize, but I encountered an issue. Please try again.');
    }
    
    // Re-enable send button
    sendBtn.disabled = false;
    messageInput.focus();
}

/**
 * Add a message to the chat
 */
function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    if (role === 'assistant') {
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="9"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
            </div>
            <div class="message-content">${formatMessage(content)}</div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-avatar">You</div>
            <div class="message-content">${escapeHtml(content)}</div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Format message content (handle line breaks, etc.)
 */
function formatMessage(content) {
    return escapeHtml(content)
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show loading indicator
 */
function showLoading() {
    isLoading = true;
    const template = document.getElementById('loadingTemplate');
    const clone = template.content.cloneNode(true);
    chatMessages.appendChild(clone);
    scrollToBottom();
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    isLoading = false;
    const loadingMessage = chatMessages.querySelector('.loading-message');
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

/**
 * Scroll to the bottom of the chat
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Reset the chat conversation
 */
function resetChat() {
    // Clear conversation history
    conversationHistory = [];
    
    // Clear messages
    chatMessages.innerHTML = '';
    
    // Show welcome card
    const welcomeHtml = `
        <div class="welcome-card" id="welcomeCard">
            <div class="welcome-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="9"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
            </div>
            <h2>Welcome to Refined Watch Insurance Advisor</h2>
            <p>I'll help you determine whether insuring your timepiece makes financial sense. Just a few quick questions, and I'll provide a personalized recommendation.</p>
            <button class="start-btn" onclick="startChat()">
                <span>Start Consultation</span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
            </button>
        </div>
    `;
    chatMessages.innerHTML = welcomeHtml;
    
    // Hide input area
    inputArea.style.display = 'none';
}

/**
 * Handle Enter key
 */
messageInput?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(e);
    }
});
