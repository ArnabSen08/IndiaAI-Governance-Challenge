// Chat functionality
let chatHistory = [];

function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    const apiKey = document.getElementById('apiKey').value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    userInput.value = '';
    
    // Show typing indicator
    addTypingIndicator();
    
    if (!apiKey) {
        // Demo mode - simulate AI response
        setTimeout(() => {
            removeTypingIndicator();
            const demoResponses = [
                "Hello! I'm a demo version of the Gemini 3 AI assistant. To experience the full capabilities, please add your API key above.",
                "This is a simulated response. The real Gemini 3 integration offers multimodal reasoning and reduced latency for amazing user experiences!",
                "I'd love to help you with that! In the full version, I can process images, answer complex questions, and provide detailed assistance.",
                "Thanks for trying the demo! The actual Gemini 3 API provides much more sophisticated responses and can handle various types of content."
            ];
            const randomResponse = demoResponses[Math.floor(Math.random() * demoResponses.length)];
            addMessageToChat('ai', randomResponse);
        }, 1500);
        return;
    }
    
    // Real API call (when API key is provided)
    callGeminiAPI(message, apiKey);
}

async function callGeminiAPI(message, apiKey) {
    try {
        // Note: In a production app, API calls should go through your backend for security
        // This is a simplified demo implementation
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${apiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: message
                    }]
                }]
            })
        });
        
        if (!response.ok) {
            throw new Error('API request failed');
        }
        
        const data = await response.json();
        removeTypingIndicator();
        
        if (data.candidates && data.candidates[0] && data.candidates[0].content) {
            const aiResponse = data.candidates[0].content.parts[0].text;
            addMessageToChat('ai', aiResponse);
        } else {
            addMessageToChat('ai', 'Sorry, I couldn\'t generate a response. Please try again.');
        }
        
    } catch (error) {
        removeTypingIndicator();
        addMessageToChat('ai', 'Sorry, there was an error connecting to the Gemini API. Please check your API key and try again.');
        console.error('API Error:', error);
    }
}

function addMessageToChat(sender, message) {
    const chatContainer = document.getElementById('chatContainer');
    
    // Clear welcome message if it's the first message
    if (chatHistory.length === 0) {
        chatContainer.innerHTML = '';
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `mb-4 ${sender === 'user' ? 'text-right' : 'text-left'}`;
    
    const messageBubble = document.createElement('div');
    messageBubble.className = `inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
        sender === 'user' 
            ? 'bg-indigo-600 text-white' 
            : 'bg-white text-gray-800 border border-gray-200'
    }`;
    
    const messageText = document.createElement('p');
    messageText.textContent = message;
    messageBubble.appendChild(messageText);
    
    const timestamp = document.createElement('div');
    timestamp.className = `text-xs text-gray-500 mt-1 ${sender === 'user' ? 'text-right' : 'text-left'}`;
    timestamp.textContent = new Date().toLocaleTimeString();
    
    messageDiv.appendChild(messageBubble);
    messageDiv.appendChild(timestamp);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    chatHistory.push({ sender, message, timestamp: new Date() });
}

function addTypingIndicator() {
    const chatContainer = document.getElementById('chatContainer');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.className = 'mb-4 text-left';
    
    const typingBubble = document.createElement('div');
    typingBubble.className = 'inline-block bg-gray-200 px-4 py-2 rounded-lg';
    
    const typingText = document.createElement('div');
    typingText.className = 'flex space-x-1';
    typingText.innerHTML = `
        <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
        <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
        <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
    `;
    
    typingBubble.appendChild(typingText);
    typingDiv.appendChild(typingBubble);
    chatContainer.appendChild(typingDiv);
    
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Enter key support
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Initialize with welcome message
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        addMessageToChat('ai', 'Welcome! I\'m your Gemini 3 AI assistant. How can I help you today?');
    }, 1000);
});