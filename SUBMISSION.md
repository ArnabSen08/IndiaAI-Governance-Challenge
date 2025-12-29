# Kiro Heroes Week 5 Submission: Bangalore Tech Culture Assistant

## Project Overview
A specialized local guide that understands Bangalore's unique tech culture, workplace dynamics, and local nuances using Kiro's agent steering capabilities.

## Challenge Requirements Met ✅

### 1. The Theme: Local Understanding
- **Focus**: Bangalore tech culture and workplace dynamics
- **Capabilities**: Tech slang translation, commute advice, food recommendations, cultural navigation
- **Local Knowledge**: Understands both traditional Bangalore culture and modern tech ecosystem

### 2. The Constraint: Custom Context File
- **File**: `.kiro/steering/product.md` ✅
- **Purpose**: Teaches Kiro about Bangalore-specific terminology, geography, and culture
- **Content**: Comprehensive local knowledge including tech hubs, slang, food culture, and work dynamics

### 3. Agent Logic: Localized Knowledge
- **Demonstrates**: How Kiro handles region-specific information
- **Examples**: Provided in `demo-examples.md` showing contextual responses
- **Testing**: `test-scenarios.py` validates local knowledge application

## Technical Implementation

### File Structure
```
├── .kiro/
│   └── steering/
│       └── product.md          # Custom context file (REQUIRED)
├── README.md                   # Project documentation
├── demo-examples.md           # Sample conversations
├── test-scenarios.py          # Test cases
├── package.json              # Project metadata
└── SUBMISSION.md             # This file
```

### Key Features
1. **Tech Slang Translator**: Understands terms like "bench time", "onsite opportunity"
2. **Geographic Navigator**: Knows routes between Koramangala, Electronic City, Whitefield
3. **Cultural Bridge**: Explains local phrases like "adjust maadi", "traffic jam aagide"
4. **Practical Advisor**: Provides real-world advice about commute, food, work culture

## Demo Scenarios
The assistant can handle queries like:
- "What does 'bench time' mean in Bangalore IT?"
- "Best route from Marathahalli to Indiranagar?"
- "Where to get South Indian breakfast near Whitefield?"
- "What's the startup culture like in Koramangala?"

## Submission Checklist ✅
- [x] `.kiro` directory included at repository root
- [x] Custom `product.md` context file created
- [x] Local guide functionality implemented
- [x] Agent steering demonstrated
- [x] Ready for GitHub repository upload
- [x] Ready for AWS Builder Center blog post

## Next Steps for Submission
1. Upload to GitHub repository (ensure `.kiro` folder is not gitignored)
2. Create AWS Builder Center blog post with screenshots/video
3. Submit both links to AI for Bharat dashboard before 11:59 PM IST

---
*Built for Kiro Heroes Week 5 Challenge - "The Local Guide"*