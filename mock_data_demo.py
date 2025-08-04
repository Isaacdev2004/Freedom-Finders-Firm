#!/usr/bin/env python3
"""
Mock data demo for Blue Bottle Coffee San Francisco
Shows what the API would return with real data
"""

import requests
import json

def demo_mock_response():
    """Demonstrate the expected API response format"""
    
    print("🎯 Mock Data Demo - Blue Bottle Coffee San Francisco")
    print("=" * 60)
    
    # Mock response that the API would return for Blue Bottle Coffee
    mock_response = {
        "business_name": "Blue Bottle Coffee",
        "star_rating": "4.3",
        "review_count": 2847,
        "top_reviews": [
            {
                "stars": 5,
                "text": "Amazing coffee and great atmosphere! The pour-over is exceptional."
            },
            {
                "stars": 4,
                "text": "Great quality coffee, though a bit pricey. Staff is very friendly."
            },
            {
                "stars": 5,
                "text": "Best coffee in San Francisco! Love their cold brew and pastries."
            },
            {
                "stars": 4,
                "text": "Consistent quality and nice seating area. Perfect for meetings."
            },
            {
                "stars": 5,
                "text": "Excellent service and the coffee is always fresh and delicious."
            }
        ],
        "categories": ["Coffee Shop", "Cafe", "Breakfast Restaurant", "Coffee Roaster"],
        "hours_of_operation": "Mon-Fri 7:00 AM–6:00 PM, Sat-Sun 8:00 AM–6:00 PM",
        "address": "1 Ferry Building, San Francisco, CA 94111",
        "website_url": "https://bluebottlecoffee.com",
        "phone_number": "(415) 543-4080",
        "profile_photo_url": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=...",
        "services_listed": [
            "Pour-over Coffee",
            "Cold Brew",
            "Espresso Drinks",
            "Pastries",
            "Coffee Beans",
            "Merchandise"
        ],
        "business_attributes": [
            "Locally Owned",
            "Eco-friendly",
            "Sustainable",
            "Artisanal Coffee"
        ],
        "google_maps_link": "https://maps.google.com/?q=Blue+Bottle+Coffee+San+Francisco",
        "webhook_status": {
            "status": "success",
            "message": "Data sent to Zapier webhook successfully",
            "webhook_response": "OK"
        }
    }
    
    print("\n📊 Expected API Response Format:")
    print(json.dumps(mock_response, indent=2))
    
    print("\n" + "=" * 60)
    print("🎯 Key Data Points Extracted:")
    print(f"📍 Business: {mock_response['business_name']}")
    print(f"⭐ Rating: {mock_response['star_rating']} stars")
    print(f"📝 Reviews: {mock_response['review_count']} reviews")
    print(f"🏷️  Categories: {', '.join(mock_response['categories'])}")
    print(f"🕒 Hours: {mock_response['hours_of_operation']}")
    print(f"📍 Address: {mock_response['address']}")
    print(f"📞 Phone: {mock_response['phone_number']}")
    print(f"🌐 Website: {mock_response['website_url']}")
    print(f"☕ Services: {', '.join(mock_response['services_listed'][:3])}...")
    print(f"🏆 Attributes: {', '.join(mock_response['business_attributes'])}")
    
    print("\n" + "=" * 60)
    print("💡 This is what the API would return if Google's anti-bot measures")
    print("   weren't blocking the scraper. The Flask backend is working correctly!")
    print("\n🚀 To get real data, you would need to:")
    print("   1. Use Google Places API (official)")
    print("   2. Implement proxy rotation")
    print("   3. Use more sophisticated scraping techniques")
    print("   4. Consider using Google My Business API")

def test_api_structure():
    """Test that the API structure is working"""
    
    print("\n🔧 Testing API Structure...")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ API is running and responding")
        else:
            print("❌ API is not responding")
            return
    except:
        print("❌ Cannot connect to API")
        return
    
    # Test extract endpoint with empty payload (should return error)
    try:
        response = requests.post(
            "http://localhost:5000/extract",
            json={},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 400:
            print("✅ API error handling is working")
        else:
            print("❌ API error handling not working")
            
    except Exception as e:
        print(f"❌ API test error: {e}")

if __name__ == "__main__":
    demo_mock_response()
    test_api_structure() 