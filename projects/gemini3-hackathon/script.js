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
        // Demo mode - simulate AI response with helpful information
        setTimeout(() => {
            removeTypingIndicator();
            const demoResponses = [
                "Hello! I'm a demo version of the Gemini 3 AI assistant. To experience the full capabilities with real Gemini 3 integration, please add your API key above or run the project locally.",
                "This is a simulated response showcasing the interface. The real Gemini 3 integration offers multimodal reasoning and reduced latency! For full functionality, download the project and run 'python run_demo.py'.",
                "I'd love to help you with that! In the full version with your API key, I can provide detailed assistance using Gemini 3's advanced capabilities. Try running locally for the best experience!",
                "Thanks for trying the demo! The actual Gemini 3 API provides sophisticated responses focused on social good. For real AI responses, add your API key or run the project locally."
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
        // Enhanced prompt for social good context
        const enhancedPrompt = `You are an AI assistant built for social good as part of the Gemini 3 Hackathon. Your responses should be helpful, ethical, and focused on positive impact.

User message: ${message}

Please provide a thoughtful and helpful response.`;

        // Try direct API call to Gemini 3 Flash Preview
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${apiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: enhancedPrompt
                    }]
                }]
            })
        });
        
        removeTypingIndicator();
        
        if (!response.ok) {
            // If the primary model fails, try fallback models
            console.log('Primary model failed, trying fallback...');
            return await tryFallbackModels(message, apiKey, enhancedPrompt);
        }
        
        const data = await response.json();
        
        if (data.candidates && data.candidates[0] && data.candidates[0].content) {
            const aiResponse = data.candidates[0].content.parts[0].text;
            addMessageToChat('ai', aiResponse);
        } else {
            addMessageToChat('ai', 'Sorry, I couldn\'t generate a response. Please try again.');
        }
        
    } catch (error) {
        removeTypingIndicator();
        console.error('API Error:', error);
        
        // Check if it's a CORS error
        if (error.message.includes('CORS') || error.message.includes('fetch')) {
            addMessageToChat('ai', `⚠️ CORS Error: Direct API calls from GitHub Pages are blocked by browser security. 
            
For the full experience:
1. Download the project locally
2. Run: python run_demo.py  
3. Open: http://localhost:8000

Or try the backend API endpoint if deployed.`);
        } else {
            addMessageToChat('ai', 'Sorry, there was an error connecting to the Gemini API. Please check your API key and try again.');
        }
    }
}

async function tryFallbackModels(message, apiKey, enhancedPrompt) {
    const fallbackModels = [
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-flash-latest'
    ];
    
    for (const model of fallbackModels) {
        try {
            console.log(`Trying fallback model: ${model}`);
            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contents: [{
                        parts: [{
                            text: enhancedPrompt
                        }]
                    }]
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.candidates && data.candidates[0] && data.candidates[0].content) {
                    const aiResponse = data.candidates[0].content.parts[0].text;
                    addMessageToChat('ai', `[Using ${model}] ${aiResponse}`);
                    return;
                }
            }
        } catch (error) {
            console.log(`Fallback model ${model} failed:`, error);
            continue;
        }
    }
    
    // If all models fail
    addMessageToChat('ai', `❌ Unable to connect to Gemini API. This might be due to:

1. **CORS restrictions** on GitHub Pages
2. **API key issues** - please verify your key
3. **Rate limiting** - please wait and try again

💡 **For best experience**: Run locally with 'python run_demo.py'`);
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
        addMessageToChat('ai', 'Welcome! I\'m your Gemini 3 AI assistant built for social good. How can I help you make a positive impact today?');
    }, 1000);
});