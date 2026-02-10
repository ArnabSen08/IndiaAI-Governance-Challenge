# The Multilingual Mandi 🏪

A real-time linguistic bridge for local trade. An AI-powered web platform that empowers local vendors with instant price discovery and smart negotiation tools.

## 🌍 Project Overview

**The Multilingual Mandi** is a web-based marketplace platform designed to help local vendors:
- List and manage their products in real-time
- Discover competitive market prices instantly
- Negotiate pricing with AI-powered assistance
- Communicate across language barriers with real-time translation
- Access market insights and analytics

### Key Features

#### 💼 Vendor Dashboard
- List products with quantities and asking prices
- Store product descriptions and details
- View all listed products with management options
- Persistent local storage of inventory

#### 🤖 AI-Powered Negotiation
- Real-time price negotiation with Gemini AI assistant
- Market-aware negotiation suggestions
- Context-aware responses based on product details
- Conversation history tracking

#### 📊 Market Price Discovery
- Real-time market pricing data for 10+ commodities
- Price ranges, averages, and trend analysis
- Market volume information
- Competitive price benchmarking

#### 🌐 Multilingual Support
- **6 Languages Supported:**
  - English 🇬🇧
  - Hindi (हिंदी) 🇮🇳
  - Spanish (Español) 🇪🇸
  - French (Français) 🇫🇷
  - Arabic (العربية) 🇸🇦
  - Portuguese (Português) 🇵🇹

#### 🔤 Real-Time Linguistic Bridge
- Market term translations
- Live chat message translation
- Language-aware responses from AI
- Seamless communication across vendors and buyers

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Google Gemini API key (optional, for enhanced features)

### Quick Start

1. **Access the Application:**
   - Visit: https://arnabsen08.github.io/multilingual-mandi/

2. **Set Your Language:**
   - Select your preferred language from the dropdown in the hero section

3. **Add an API Key (Optional):**
   - Get a free Gemini API key: https://aistudio.google.com/app/apikey
   - Paste it in the API setup section
   - The app works with or without the API key (uses mock data if not provided)

4. **List Your Products:**
   - Enter product name, quantity, price, and description
   - Click "List Product"
   - Your products are automatically saved

5. **Discover Market Prices:**
   - View real-time market prices in the "Market Prices" section
   - Compare your pricing with market averages

6. **Negotiate Prices:**
   - Use the AI assistant to get negotiation suggestions
   - Ask questions about fair pricing
   - Get market-aware recommendations

7. **Translate Market Terms:**
   - Use the linguistic bridge to translate trading terms
   - Communicate in your native language

## 🏗️ Project Structure

```
.
├── index.html           # Main application HTML
├── styles.css          # Responsive CSS styling
├── app.js              # Core application logic with Gemini integration
├── README.md           # Comprehensive project documentation
├── QUICK_START.md      # Quick setup guide
├── GITHUB_SETUP.md     # Manual GitHub setup instructions
└── .github/
    └── workflows/
        └── pages.yml   # GitHub Pages deployment workflow
```

## 🔧 Features & Functionality

### Product Management
- Add unlimited products to your inventory
- Edit product listings
- Delete products when sold
- Automatic timestamp tracking

### Market Analysis
- Compare your prices with market data
- View price trends (up/down/stable)
- Monitor market volume
- Get pricing recommendations

### AI Negotiation
- Conversational negotiation interface
- Context-aware responses
- Real-time market data integration
- Multiple negotiation strategies

### Translation Services
- **Market Term Translation:** Translate specific trading terms
- **Chat Translation:** Translate full messages and conversations
- Support for 6 different languages
- Real-time translation as you type

## 🤖 Gemini API Integration

### Using with API Key
When you provide a Gemini API key, the app uses advanced AI models for:
- Context-aware negotiation advice
- Accurate market-aware responses
- Natural language understanding
- Semantic translation

### Using without API Key
The app works perfectly without an API key using:
- Pre-trained mock negotiation responses
- Basic translation mappings
- Simulated market analysis

## 💾 Data Storage

All your data is stored locally in your browser:
- Products are saved to browser localStorage
- No data is sent to external servers (unless using Gemini API)
- Your data persists across browser sessions
- Clear your browser data to reset the app

## 🌐 Multilingual Examples

### Hindi Support (हिंदी)
- उत्पाद जोड़ें (Add Product)
- बाजार कीमतें (Market Prices)
- AI सहायक (AI Assistant)

### Spanish Support (Español)
- Agregar Producto
- Precios de Mercado
- Asistente de IA

...and 4 more languages with full UI translations!

## 📱 Responsive Design

- **Desktop:** Full-featured interface with multi-column layouts
- **Tablet:** Optimized 2-column layout
- **Mobile:** Single column, touch-friendly interface

## 🔐 Privacy & Security

- All product data stored locally in your browser
- No account creation required
- API key stored locally (you control sharing)
- No tracking or analytics
- HTTPS connection via GitHub Pages

## 🎯 Use Cases

### For Individual Vendors
- List seasonal produce as it becomes available
- Compare your prices with market rates
- Get negotiation tips for fair pricing

### For Vendor Cooperatives
- Aggregate products from multiple members
- Access collective market data
- Coordinate pricing strategies

### For Buyers/Brokers
- Find products from local vendors
- Assess market prices
- Initiate negotiations

### For Market Researchers
- Monitor local price trends
- Track market volume
- Analyze vendor behavior

## 🚀 Deployment

### Live Site
The application is automatically deployed via GitHub Pages:
- **URL:** https://arnabsen08.github.io/multilingual-mandi/
- **Updates:** Automatically deployed when you push to main branch
- **Build Time:** Usually live within 1-2 minutes

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/ArnabSen08/multilingual-mandi.git
   cd multilingual-mandi
   ```

2. Open `index.html` in your browser
3. No build process needed!

## 🔧 Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **API:** Google Gemini API (optional)
- **Storage:** Browser localStorage
- **Hosting:** GitHub Pages
- **CI/CD:** GitHub Actions

## 📚 API Documentation

### Gemini API Endpoint
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
```

### Required Headers
```
Content-Type: application/json
Authorization: Bearer {API_KEY}
```

### Request Payload
```json
{
  "contents": [{
    "parts": [{
      "text": "Your prompt here"
    }]
  }],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 200
  }
}
```

## 🐛 Known Limitations

- Market data is simulated (not real-time)
- Chat history is lost on page refresh
- Translation is basic without API key
- Support for 6 languages (extensible)

## 🎓 Educational Purpose

This project demonstrates:
- Modern JavaScript ES6+ patterns
- API integration with Google Cloud
- Multilingual web application design
- Real-time data handling
- Responsive web design
- Local storage management

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Real market data API integration
- User authentication system
- Database backend
- Mobile app version
- Additional languages
- Advanced analytics
- Payment integration

## 📄 License

This project is open source and available for educational and commercial use.

## 👨‍💻 Author

Created for the **26 Jan Prompt Challenge 2026**
Challenge: Creating a Real-time Linguistic Bridge for Local Trade

## 🙏 Acknowledgments

- **Google Gemini AI** for advanced language models
- **GitHub Pages** for free hosting
- **Local vendor communities** for inspiration
- Open source community for tools and libraries

## 📞 Support

For issues, questions, or suggestions:
1. Check [QUICK_START.md](QUICK_START.md) for setup help
2. Review [GITHUB_SETUP.md](GITHUB_SETUP.md) for GitHub issues
3. Open an issue on GitHub
4. Check browser console for error messages

## 🚀 Future Roadmap

- [ ] Real-time market data integration
- [ ] User accounts and authentication
- [ ] Database backend (Firebase/Supabase)
- [ ] Mobile app (React Native/Flutter)
- [ ] Payment processing
- [ ] Ratings and reviews system
- [ ] Video marketplace
- [ ] Blockchain price verification
- [ ] IoT sensor integration
- [ ] Export to PDF reports

---

**Built with ❤️ for local vendors worldwide | Empowering trade through technology**
