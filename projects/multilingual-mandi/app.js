// The Multilingual Mandi - JavaScript Application
// Integrated with Google Gemini API for AI-powered features

class MultilingualMandi {
    constructor() {
        this.apiKey = localStorage.getItem('gemini_api_key') || '';
        this.currentLanguage = localStorage.getItem('language') || 'en';
        this.products = JSON.parse(localStorage.getItem('mandi_products')) || [];
        this.marketData = this.initializeMarketData();
        this.chatHistory = [];
        this.conversationContext = '';
        
        this.init();
    }

    init() {
        this.loadProducts();
        this.updateMarketPrices();
        this.setupEventListeners();
        this.displayLanguage();
    }

    // Language and Localization
    setLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('language', lang);
        this.displayLanguage();
        this.updateUIText();
    }

    displayLanguage() {
        const langSelect = document.getElementById('language');
        if (langSelect) {
            langSelect.value = this.currentLanguage;
        }
    }

    updateUIText() {
        const translations = {
            en: {
                addProduct: "Add Your Product",
                productName: "Product name (e.g., Tomatoes)",
                quantity: "Quantity",
                price: "Your asking price",
                description: "Product description (optional)",
                listProduct: "List Product",
                yourProducts: "Your Listed Products",
                marketAnalysis: "Market Price Analysis",
                selectProduct: "Select a product to analyze market prices...",
                negotiateAI: "Negotiate with AI Assistant",
                askPrice: "Ask about prices or negotiate...",
                send: "Send",
                marketPrices: "Market Prices",
                translateTerms: "Translate Market Terms",
                enterTerm: "Enter a market term...",
                translate: "Translate",
                chatTranslation: "Real-Time Chat Translation",
                enterMessage: "Enter message to translate..."
            },
            hi: {
                addProduct: "अपना उत्पाद जोड़ें",
                productName: "उत्पाद का नाम (जैसे, टमाटर)",
                quantity: "मात्रा",
                price: "आपकी मांगी गई कीमत",
                description: "उत्पाद विवरण (वैकल्पिक)",
                listProduct: "उत्पाद सूचीबद्ध करें",
                yourProducts: "आपके सूचीबद्ध उत्पाद",
                marketAnalysis: "बाजार मूल्य विश्लेषण",
                selectProduct: "बाजार मूल्य विश्लेषण के लिए एक उत्पाद चुनें...",
                negotiateAI: "AI सहायक के साथ बातचीत करें",
                askPrice: "कीमतों के बारे में पूछें या बातचीत करें...",
                send: "भेजें",
                marketPrices: "बाजार कीमतें",
                translateTerms: "बाजार शर्तों का अनुवाद करें",
                enterTerm: "बाजार शब्द दर्ज करें...",
                translate: "अनुवाद करें",
                chatTranslation: "वास्तविक समय चैट अनुवाद",
                enterMessage: "अनुवाद करने के लिए संदेश दर्ज करें..."
            },
            es: {
                addProduct: "Agregar Tu Producto",
                productName: "Nombre del producto (p. ej., Tomates)",
                quantity: "Cantidad",
                price: "Tu precio solicitado",
                description: "Descripción del producto (opcional)",
                listProduct: "Listar Producto",
                yourProducts: "Tus Productos Listados",
                marketAnalysis: "Análisis de Precios de Mercado",
                selectProduct: "Selecciona un producto para analizar precios de mercado...",
                negotiateAI: "Negociar con Asistente de IA",
                askPrice: "Pregunta sobre precios o negocia...",
                send: "Enviar",
                marketPrices: "Precios de Mercado",
                translateTerms: "Traducir Términos de Mercado",
                enterTerm: "Ingresa un término de mercado...",
                translate: "Traducir",
                chatTranslation: "Traducción de Chat en Tiempo Real",
                enterMessage: "Ingresa el mensaje a traducir..."
            }
        };

        // Update UI with translations
        const trans = translations[this.currentLanguage] || translations['en'];
        
        // Update placeholders and labels
        const elements = {
            'productName': trans.productName,
            'productQuantity': trans.quantity,
            'productPrice': trans.price,
            'productDescription': trans.description,
            'negotiationInput': trans.askPrice,
            'termToTranslate': trans.enterTerm,
            'chatText': trans.enterMessage
        };

        for (const [id, text] of Object.entries(elements)) {
            const elem = document.getElementById(id);
            if (elem) elem.placeholder = text;
        }
    }

    // API Key Management
    setApiKey() {
        const keyInput = document.getElementById('apiKey');
        const statusDiv = document.getElementById('apiStatus');
        
        if (keyInput.value.trim()) {
            this.apiKey = keyInput.value.trim();
            localStorage.setItem('gemini_api_key', this.apiKey);
            
            statusDiv.textContent = '✓ API Key saved successfully!';
            statusDiv.className = 'status-message success';
            keyInput.value = '';
            
            setTimeout(() => {
                statusDiv.className = 'status-message';
            }, 5000);
        } else {
            statusDiv.textContent = '✗ Please enter a valid API key';
            statusDiv.className = 'status-message error';
        }
    }

    // Product Management
    addProduct() {
        const name = document.getElementById('productName').value;
        const quantity = document.getElementById('productQuantity').value;
        const unit = document.getElementById('quantityUnit').value;
        const price = document.getElementById('productPrice').value;
        const currency = document.getElementById('currency').value;
        const description = document.getElementById('productDescription').value;

        if (!name || !quantity || !price) {
            alert('Please fill in all required fields');
            return;
        }

        const product = {
            id: Date.now(),
            name: name,
            quantity: quantity,
            unit: unit,
            price: parseFloat(price),
            currency: currency,
            description: description,
            timestamp: new Date().toLocaleString()
        };

        this.products.push(product);
        this.saveProducts();
        this.loadProducts();
        this.clearProductForm();
    }

    clearProductForm() {
        document.getElementById('productName').value = '';
        document.getElementById('productQuantity').value = '';
        document.getElementById('productPrice').value = '';
        document.getElementById('productDescription').value = '';
    }

    saveProducts() {
        localStorage.setItem('mandi_products', JSON.stringify(this.products));
    }

    loadProducts() {
        const list = document.getElementById('productsList');
        list.innerHTML = '';

        if (this.products.length === 0) {
            list.innerHTML = '<p style="text-align: center; color: #999;">No products listed yet</p>';
            return;
        }

        this.products.forEach(product => {
            const item = document.createElement('div');
            item.className = 'product-item';
            item.innerHTML = `
                <h5>${product.name}</h5>
                <p><strong>Quantity:</strong> ${product.quantity} ${product.unit}</p>
                <p><strong>Price:</strong> ${product.currency} ${product.price.toFixed(2)}</p>
                ${product.description ? `<p><strong>Description:</strong> ${product.description}</p>` : ''}
                <p style="font-size: 0.85rem; color: #999;">Listed: ${product.timestamp}</p>
                <div class="product-actions">
                    <button onclick="app.negotiateProduct(${product.id})" class="btn-secondary">Negotiate</button>
                    <button onclick="app.deleteProduct(${product.id})" class="btn-danger">Remove</button>
                </div>
            `;
            list.appendChild(item);
        });
    }

    deleteProduct(id) {
        this.products = this.products.filter(p => p.id !== id);
        this.saveProducts();
        this.loadProducts();
    }

    negotiateProduct(id) {
        const product = this.products.find(p => p.id === id);
        if (product) {
            this.conversationContext = `I'm selling ${product.quantity} ${product.unit} of ${product.name} at ${product.currency} ${product.price}. ${product.description || ''}`;
            document.getElementById('negotiationInput').value = `Tell me fair market price for ${product.name}`;
            this.sendNegotiation();
            document.querySelector('.negotiation').scrollIntoView({ behavior: 'smooth' });
        }
    }

    // Market Data
    initializeMarketData() {
        return {
            'Tomatoes': { low: 0.5, high: 2.0, avg: 1.2, trend: 'down', volume: '1200 units' },
            'Rice': { low: 8.0, high: 15.0, avg: 11.5, trend: 'stable', volume: '500 units' },
            'Wheat': { low: 6.0, high: 12.0, avg: 9.0, trend: 'up', volume: '800 units' },
            'Onions': { low: 0.3, high: 1.5, avg: 0.8, trend: 'up', volume: '900 units' },
            'Potatoes': { low: 0.2, high: 1.0, avg: 0.6, trend: 'down', volume: '1100 units' },
            'Carrots': { low: 0.4, high: 1.2, avg: 0.8, trend: 'stable', volume: '600 units' },
            'Cabbage': { low: 0.2, high: 0.8, avg: 0.5, trend: 'down', volume: '700 units' },
            'Milk': { low: 0.8, high: 2.5, avg: 1.8, trend: 'stable', volume: '2000 liters' },
            'Eggs': { low: 0.05, high: 0.15, avg: 0.10, trend: 'stable', volume: '5000 units' },
            'Fish': { low: 3.0, high: 8.0, avg: 5.5, trend: 'up', volume: '300 units' }
        };
    }

    updateMarketPrices() {
        const container = document.getElementById('marketPrices');
        container.innerHTML = '';

        for (const [name, data] of Object.entries(this.marketData)) {
            const card = document.createElement('div');
            card.className = 'price-card';
            const trendIcon = data.trend === 'up' ? '📈' : data.trend === 'down' ? '📉' : '➡️';
            const trendClass = data.trend === 'up' ? 'trend-up' : 'trend-down';

            card.innerHTML = `
                <h5>${name}</h5>
                <div class="price-display">$${data.avg.toFixed(2)}</div>
                <p><strong>Range:</strong> $${data.low.toFixed(2)} - $${data.high.toFixed(2)}</p>
                <p class="price-trend ${trendClass}"><span>${trendIcon}</span> ${data.trend}</p>
                <p style="font-size: 0.85rem; color: #999;">Volume: ${data.volume}</p>
            `;
            container.appendChild(card);
        }
    }

    // AI Negotiation with Gemini
    async sendNegotiation() {
        const input = document.getElementById('negotiationInput');
        const message = input.value.trim();

        if (!message) return;

        // Add user message to chat
        this.addChatMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        this.addChatMessage('Thinking...', 'system');

        try {
            if (this.apiKey) {
                // Use Gemini API
                const response = await this.callGeminiAPI(message);
                this.chatHistory.pop(); // Remove typing indicator
                this.addChatMessage(response, 'assistant');
            } else {
                // Use mock response
                this.chatHistory.pop(); // Remove typing indicator
                const mockResponse = this.generateMockNegotiationResponse(message);
                this.addChatMessage(mockResponse, 'assistant');
            }
        } catch (error) {
            this.chatHistory.pop(); // Remove typing indicator
            this.addChatMessage('Error: Could not get response. Please check your API key.', 'assistant');
            console.error('Error:', error);
        }
    }

    async callGeminiAPI(message) {
        const endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent';
        
        const payload = {
            contents: [{
                parts: [{
                    text: `You are an expert market negotiator helping local vendors. 
                    Current context: ${this.conversationContext}
                    User message: ${message}
                    
                    Provide helpful, brief advice about pricing and negotiation in ${this.currentLanguage}.
                    Keep responses concise and practical.`
                }]
            }],
            generationConfig: {
                temperature: 0.7,
                maxOutputTokens: 200
            }
        };

        const response = await fetch(`${endpoint}?key=${this.apiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        return data.candidates[0].content.parts[0].text;
    }

    generateMockNegotiationResponse(message) {
        const mockResponses = [
            "Based on current market trends, that's a competitive price. Consider seasonal demand variations.",
            "The market average is slightly lower. You might want to adjust your price or highlight unique qualities.",
            "Good choice! This product category is seeing stable demand. Your pricing is fair.",
            "Market data shows demand is increasing for this product. Hold your price or consider a premium.",
            "Consider bulk discounts to attract larger buyers. This is a proven strategy in local markets.",
            "Your quantity is attractive. Focus on quality and freshness to justify your current price.",
            "Check nearby vendors for comparative pricing. Differentiation is key in local trade.",
            "This product has seasonal variations. Track price trends and adjust accordingly."
        ];
        return mockResponses[Math.floor(Math.random() * mockResponses.length)];
    }

    addChatMessage(text, sender) {
        const container = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
        
        this.chatHistory.push({ sender, text });
    }

    // Translation Services
    async translateTerm() {
        const term = document.getElementById('termToTranslate').value.trim();
        const targetLang = document.getElementById('targetLanguage').value;
        const resultDiv = document.getElementById('translationResult');

        if (!term) {
            resultDiv.classList.remove('show');
            return;
        }

        try {
            if (this.apiKey) {
                const translation = await this.callGeminiTranslate(term, targetLang);
                resultDiv.innerHTML = `
                    <div class="translation-item">
                        <div class="translation-label">Original: </div>
                        <div class="translation-text">${term}</div>
                    </div>
                    <div class="translation-item">
                        <div class="translation-label">Translation: </div>
                        <div class="translation-text">${translation}</div>
                    </div>
                `;
            } else {
                const translation = this.generateMockTranslation(term, targetLang);
                resultDiv.innerHTML = `
                    <div class="translation-item">
                        <div class="translation-label">Original: </div>
                        <div class="translation-text">${term}</div>
                    </div>
                    <div class="translation-item">
                        <div class="translation-label">Translation: </div>
                        <div class="translation-text">${translation}</div>
                    </div>
                `;
            }
            resultDiv.classList.add('show');
        } catch (error) {
            resultDiv.innerHTML = '<p style="color: red;">Translation error. Please try again.</p>';
            resultDiv.classList.add('show');
            console.error('Translation error:', error);
        }
    }

    async callGeminiTranslate(text, targetLang) {
        const endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent';
        
        const langMap = { en: 'English', hi: 'Hindi', es: 'Spanish', fr: 'French', ar: 'Arabic', pt: 'Portuguese' };
        
        const payload = {
            contents: [{
                parts: [{
                    text: `Translate this market/trading term to ${langMap[targetLang]}: "${text}". Provide only the translation.`
                }]
            }]
        };

        const response = await fetch(`${endpoint}?key=${this.apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Translation API error');

        const data = await response.json();
        return data.candidates[0].content.parts[0].text;
    }

    generateMockTranslation(term, targetLang) {
        const translations = {
            'wholesale': { hi: 'थोक', es: 'venta al por mayor', fr: 'gros', ar: 'جملة' },
            'price': { hi: 'कीमत', es: 'precio', fr: 'prix', ar: 'سعر' },
            'market': { hi: 'बाजार', es: 'mercado', fr: 'marché', ar: 'سوق' },
            'negotiate': { hi: 'बातचीत करना', es: 'negociar', fr: 'négocier', ar: 'التفاوض' },
            'quality': { hi: 'गुणवत्ता', es: 'calidad', fr: 'qualité', ar: 'جودة' }
        };

        return translations[term.toLowerCase()]?.[targetLang] || `[${term} in ${targetLang}]`;
    }

    async translateChat() {
        const text = document.getElementById('chatText').value.trim();
        const targetLang = document.getElementById('chatTargetLang').value;
        const resultDiv = document.getElementById('chatTranslationResult');

        if (!text) {
            resultDiv.classList.remove('show');
            return;
        }

        try {
            if (this.apiKey) {
                const translation = await this.callGeminiTranslate(text, targetLang);
                resultDiv.innerHTML = `
                    <div class="translation-item">
                        <div class="translation-label">Original: </div>
                        <div class="translation-text">${text}</div>
                    </div>
                    <div class="translation-item">
                        <div class="translation-label">Translated: </div>
                        <div class="translation-text">${translation}</div>
                    </div>
                `;
            } else {
                // Mock translation
                const translated = text.split(' ').map(word => `[${word}]`).join(' ');
                resultDiv.innerHTML = `
                    <div class="translation-item">
                        <div class="translation-label">Original: </div>
                        <div class="translation-text">${text}</div>
                    </div>
                    <div class="translation-item">
                        <div class="translation-label">Translated: </div>
                        <div class="translation-text">${translated}</div>
                    </div>
                `;
            }
            resultDiv.classList.add('show');
        } catch (error) {
            resultDiv.innerHTML = '<p style="color: red;">Translation error. Please try again.</p>';
            resultDiv.classList.add('show');
        }
    }

    // Event Listeners
    setupEventListeners() {
        // Product form
        const productForm = document.querySelector('.add-product');
        if (productForm) {
            productForm.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                    this.addProduct();
                }
            });
        }

        // Negotiation input
        const negotiationInput = document.getElementById('negotiationInput');
        if (negotiationInput) {
            negotiationInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendNegotiation();
                }
            });
        }

        // Translation inputs
        const termInput = document.getElementById('termToTranslate');
        const chatInput = document.getElementById('chatText');
        
        if (termInput) {
            termInput.addEventListener('input', () => {
                this.translateTerm();
            });
        }
        
        if (chatInput) {
            chatInput.addEventListener('input', () => {
                // Auto-translate on input change
                if (chatInput.value.trim()) {
                    this.translateChat();
                }
            });
        }
    }
}

// Initialize the app
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new MultilingualMandi();
    
    // Make functions available globally
    window.setLanguage = (lang) => app.setLanguage(lang);
    window.setApiKey = () => app.setApiKey();
    window.addProduct = () => app.addProduct();
    window.deleteProduct = (id) => app.deleteProduct(id);
    window.negotiateProduct = (id) => app.negotiateProduct(id);
    window.sendNegotiation = () => app.sendNegotiation();
    window.translateTerm = () => app.translateTerm();
    window.translateChat = () => app.translateChat();
});
