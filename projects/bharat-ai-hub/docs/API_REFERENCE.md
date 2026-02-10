# API Reference - Bharat AI Hub

Base URL: `https://api.bharataihub.com` (Production)  
Base URL: `http://localhost:3000` (Development)

## Authentication

All API requests require authentication using JWT tokens.

```bash
# Get token
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

# Use token in requests
Authorization: Bearer <your_jwt_token>
```

## Healthcare Module APIs

### 1. AI Diagnosis Assistant

Generate AI-powered diagnosis suggestions based on symptoms.

**Endpoint:** `POST /api/healthcare/diagnosis`

**Request:**
```json
{
  "symptoms": "fever, cough, headache",
  "medicalHistory": {
    "age": 35,
    "gender": "male",
    "conditions": ["diabetes"],
    "medications": ["metformin"]
  },
  "patientId": 123
}
```

**Response:**
```json
{
  "success": true,
  "diagnosis": {
    "possibleConditions": [
      {
        "condition": "Viral Infection",
        "probability": 0.75,
        "description": "Common viral infection with flu-like symptoms"
      },
      {
        "condition": "COVID-19",
        "probability": 0.15,
        "description": "Coronavirus infection"
      }
    ],
    "recommendedTests": [
      "Complete Blood Count",
      "COVID-19 RT-PCR"
    ],
    "generalAdvice": "Rest, hydration, monitor temperature",
    "urgency": "moderate"
  },
  "disclaimer": "This is an AI-generated preliminary assessment..."
}
```

### 2. Upload Prescription

Upload and extract text from prescription images.

**Endpoint:** `POST /api/healthcare/prescription/upload`

**Request:**
```json
{
  "patientId": 123,
  "prescriptionImage": "base64_encoded_image_data"
}
```

**Response:**
```json
{
  "success": true,
  "imageUrl": "https://s3.amazonaws.com/...",
  "extractedData": {
    "rawText": "Dr. John Smith\nMedicine: Paracetamol 500mg...",
    "medicines": [
      {
        "name": "Paracetamol",
        "dosage": "500mg",
        "frequency": "3 times daily"
      }
    ],
    "doctorName": "Dr. John Smith",
    "date": "2026-01-15"
  }
}
```

### 3. Get Patient Records

Retrieve patient medical history.

**Endpoint:** `GET /api/healthcare/patient/:patientId/records`

**Response:**
```json
{
  "success": true,
  "patient": {
    "id": 123,
    "name": "John Doe",
    "age": 35,
    "gender": "male",
    "contact": "+91-9876543210"
  },
  "diagnoses": [...],
  "prescriptions": [...],
  "appointments": [...]
}
```

## Rural Module APIs

### 1. Crop Advisory

Get AI-powered crop recommendations.

**Endpoint:** `POST /api/rural/crop-advisory`

**Request:**
```json
{
  "farmerId": 456,
  "farmData": {
    "soilType": "loamy",
    "location": "Punjab",
    "season": "kharif",
    "previousCrop": "wheat",
    "landSize": 5.5,
    "resources": {
      "irrigation": "available",
      "equipment": ["tractor", "harvester"]
    }
  },
  "language": "pa"
}
```

**Response:**
```json
{
  "success": true,
  "advisory": {
    "recommendedCrops": [
      {
        "crop": "Rice",
        "suitability": 0.92,
        "expectedYield": "4.5 tons/hectare",
        "marketPrice": "₹2,500/quintal"
      }
    ],
    "plantingSchedule": {
      "preparation": "June 1-15",
      "sowing": "June 15-30",
      "harvest": "October 15-30"
    },
    "fertilizers": [...],
    "pestManagement": [...],
    "estimatedIncome": "₹2,47,500"
  },
  "language": "pa"
}
```

### 2. Crop Disease Detection

Detect diseases from crop images.

**Endpoint:** `POST /api/rural/crop-disease/detect`

**Request:**
```json
{
  "farmerId": 456,
  "cropImage": "base64_encoded_image",
  "cropType": "rice"
}
```

**Response:**
```json
{
  "success": true,
  "imageUrl": "https://s3.amazonaws.com/...",
  "analysis": {
    "detected": true,
    "disease": "Leaf Blight",
    "confidence": 0.87,
    "severity": "moderate",
    "treatment": "Apply fungicide and remove affected leaves",
    "preventiveMeasures": [...]
  }
}
```

### 3. Market Prices

Get current market prices for crops.

**Endpoint:** `GET /api/rural/market-prices?location=Punjab&cropType=rice`

**Response:**
```json
{
  "success": true,
  "currentPrice": 2500,
  "averagePrice": 2350,
  "trend": "increasing",
  "history": [
    {
      "date": "2026-01-15",
      "price": 2500,
      "location": "Punjab"
    }
  ]
}
```

## Retail Module APIs

### 1. Demand Forecasting

Get demand forecast for products.

**Endpoint:** `POST /api/retail/forecast`

**Request:**
```json
{
  "productId": 789,
  "timeframe": "30days",
  "historicalData": {
    "sales": [...],
    "seasonality": "high",
    "events": ["festival", "sale"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "forecast": {
    "predictedDemand": 1500,
    "confidence": 0.85,
    "trend": "increasing",
    "recommendations": {
      "stockLevel": 1800,
      "reorderPoint": 500,
      "optimalPrice": 499
    }
  }
}
```

### 2. Dynamic Pricing

Get optimal pricing recommendations.

**Endpoint:** `POST /api/retail/pricing`

**Request:**
```json
{
  "productId": 789,
  "currentPrice": 500,
  "competitorPrices": [480, 520, 495],
  "inventory": 200,
  "demand": "high"
}
```

**Response:**
```json
{
  "success": true,
  "recommendedPrice": 510,
  "priceRange": {
    "min": 490,
    "max": 530
  },
  "expectedRevenue": 102000,
  "reasoning": "High demand with moderate competition"
}
```

## Learning Module APIs

### 1. Generate Learning Path

Create personalized learning path.

**Endpoint:** `POST /api/learning/path/generate`

**Request:**
```json
{
  "studentId": 321,
  "profile": {
    "currentLevel": "beginner",
    "goal": "Full Stack Developer",
    "availableTime": 10,
    "learningStyle": "visual",
    "interests": ["web development", "databases"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "learningPath": {
    "duration": "6 months",
    "curriculum": [
      {
        "week": 1,
        "topic": "HTML & CSS Basics",
        "resources": [...],
        "exercises": [...],
        "estimatedHours": 10
      }
    ],
    "milestones": [...],
    "assessments": [...]
  }
}
```

### 2. AI Tutor

Ask questions to AI tutor.

**Endpoint:** `POST /api/learning/tutor/ask`

**Request:**
```json
{
  "studentId": 321,
  "question": "Explain closures in JavaScript",
  "context": "learning-javascript",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "answer": "A closure is a function that has access to variables...",
  "examples": [...],
  "relatedTopics": ["scope", "hoisting"],
  "practiceExercises": [...]
}
```

## Content Module APIs

### 1. Generate Content

Generate content using AI.

**Endpoint:** `POST /api/content/generate`

**Request:**
```json
{
  "topic": "Benefits of AI in Healthcare",
  "format": "blog",
  "language": "hi",
  "length": "medium",
  "tone": "informative"
}
```

**Response:**
```json
{
  "success": true,
  "content": "स्वास्थ्य सेवा में AI के लाभ...",
  "metadata": {
    "wordCount": 500,
    "readingTime": "3 minutes",
    "keywords": [...]
  }
}
```

### 2. Translate Content

Translate content to multiple languages.

**Endpoint:** `POST /api/content/translate`

**Request:**
```json
{
  "text": "Welcome to Bharat AI Hub",
  "targetLanguages": ["hi", "ta", "te", "bn"],
  "sourceLanguage": "en"
}
```

**Response:**
```json
{
  "success": true,
  "translations": {
    "hi": "भारत AI हब में आपका स्वागत है",
    "ta": "பாரத் AI ஹப்பிற்கு வரவேற்கிறோம்",
    "te": "భారత్ AI హబ్‌కు స్వాగతం",
    "bn": "ভারত AI হাবে স্বাগতম"
  }
}
```

## Community Module APIs

### 1. Submit Grievance

Submit a community grievance.

**Endpoint:** `POST /api/community/grievance/submit`

**Request:**
```json
{
  "userId": 654,
  "category": "infrastructure",
  "description": "Street lights not working in sector 5",
  "location": {
    "latitude": 28.7041,
    "longitude": 77.1025
  },
  "attachments": ["image1.jpg"]
}
```

**Response:**
```json
{
  "success": true,
  "grievanceId": 9876,
  "analysis": {
    "category": "infrastructure",
    "priority": "medium",
    "department": "Municipal Corporation",
    "estimatedResolution": "7 days"
  },
  "ticketNumber": "GRV-2026-9876"
}
```

### 2. Track Grievance

Track grievance status.

**Endpoint:** `GET /api/community/grievance/:grievanceId/status`

**Response:**
```json
{
  "success": true,
  "grievance": {
    "id": 9876,
    "status": "in-progress",
    "assignedTo": "Municipal Engineer",
    "updates": [
      {
        "date": "2026-01-15",
        "status": "submitted",
        "note": "Grievance received"
      },
      {
        "date": "2026-01-16",
        "status": "in-progress",
        "note": "Team assigned for inspection"
      }
    ],
    "expectedResolution": "2026-01-22"
  }
}
```

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

### Common Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## Rate Limiting

- **Free Tier**: 100 requests/hour
- **Basic Tier**: 1,000 requests/hour
- **Premium Tier**: 10,000 requests/hour
- **Enterprise**: Unlimited

## Webhooks

Subscribe to events:

```json
POST /api/webhooks/subscribe
{
  "url": "https://your-domain.com/webhook",
  "events": ["diagnosis.completed", "grievance.resolved"],
  "secret": "your_webhook_secret"
}
```

## SDKs

Official SDKs available for:
- JavaScript/Node.js
- Python
- Java
- Go

```bash
npm install @bharat-ai-hub/sdk
```

## Support

- Documentation: https://docs.bharataihub.com
- API Status: https://status.bharataihub.com
- Support Email: api-support@bharataihub.com
