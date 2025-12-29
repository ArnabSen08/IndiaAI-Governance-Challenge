#!/usr/bin/env python3
"""
Test scenarios for Bangalore Tech Culture Assistant
Demonstrates the local knowledge and cultural understanding
"""

def test_local_guide():
    """
    Test scenarios that showcase the assistant's understanding of Bangalore tech culture
    """
    
    test_cases = [
        {
            "category": "Tech Slang",
            "input": "What's an onsite opportunity?",
            "expected_context": "Should explain client location work abroad, high value in Bangalore IT"
        },
        {
            "category": "Geography",
            "input": "How do I get from Marathahalli to Koramangala?",
            "expected_context": "Should mention traffic, routes, and local transport options"
        },
        {
            "category": "Food Culture", 
            "input": "Where can I get good dosa near Electronic City?",
            "expected_context": "Should recommend local places, mention office food courts"
        },
        {
            "category": "Work Culture",
            "input": "What should I wear to a Bangalore IT company?",
            "expected_context": "Should differentiate between service companies and startups"
        },
        {
            "category": "Local Language",
            "input": "Someone said 'adjust maadi' - what does that mean?",
            "expected_context": "Should explain Kannada phrase meaning and usage context"
        }
    ]
    
    print("🏢 Bangalore Tech Culture Assistant - Test Scenarios")
    print("=" * 50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['category']} Test:")
        print(f"   Input: {test['input']}")
        print(f"   Expected: {test['expected_context']}")
    
    print("\n✅ These scenarios test the assistant's ability to:")
    print("   - Understand local tech terminology")
    print("   - Provide geographic and cultural context")
    print("   - Bridge language and cultural gaps")
    print("   - Give practical, location-specific advice")

if __name__ == "__main__":
    test_local_guide()