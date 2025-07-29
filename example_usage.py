#!/usr/bin/env python3
"""
Example usage script for Google Business Scraper API
Demonstrates how to use the API with different types of inputs
"""

import requests
import json
import time

# API base URL (change this to your deployed URL)
API_BASE_URL = "http://localhost:5000"  # Change to your deployed URL

def test_business_extraction():
    """Test business extraction with different inputs"""
    
    print("🚀 Google Business Scraper - Example Usage")
    print("=" * 50)
    
    # Example 1: Extract by business name
    print("\n1. Extracting business data by name...")
    payload = {
        "business_name": "Freedom Finders Firm"
    }
    
    response = make_api_request("/extract", payload)
    if response:
        print("✅ Business extraction successful!")
        print_business_summary(response)
    
    # Example 2: Extract by website URL
    print("\n2. Extracting business data by website URL...")
    payload = {
        "website_url": "https://freedomfindersfirm.com"
    }
    
    response = make_api_request("/extract", payload)
    if response:
        print("✅ Website extraction successful!")
        print_business_summary(response)
    
    # Example 3: Test with a real business (you can change this)
    print("\n3. Testing with a real business...")
    payload = {
        "business_name": "Starbucks"  # Change to any real business
    }
    
    response = make_api_request("/extract", payload)
    if response:
        print("✅ Real business extraction successful!")
        print_business_summary(response)
    
    # Example 4: Test error handling
    print("\n4. Testing error handling...")
    payload = {}  # Empty payload should return error
    
    response = make_api_request("/extract", payload)
    if response and 'error' in response:
        print("✅ Error handling working correctly!")
        print(f"   Error: {response['error']}")

def make_api_request(endpoint, payload):
    """Make API request and handle response"""
    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"⚠️  Business not found (status: {response.status_code})")
            return response.json()
        elif response.status_code == 400:
            print(f"❌ Bad request (status: {response.status_code})")
            return response.json()
        else:
            print(f"❌ API request failed (status: {response.status_code})")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running!")
        return None
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The server might be slow.")
        return None
    except Exception as e:
        print(f"❌ Request error: {e}")
        return None

def print_business_summary(data):
    """Print a summary of business data"""
    if 'error' in data:
        print(f"   Error: {data['error']}")
        return
    
    print(f"   📍 Business: {data.get('business_name', 'N/A')}")
    print(f"   ⭐ Rating: {data.get('star_rating', 'N/A')}")
    print(f"   📝 Reviews: {data.get('review_count', 'N/A')}")
    print(f"   📍 Address: {data.get('address', 'N/A')}")
    print(f"   📞 Phone: {data.get('phone_number', 'N/A')}")
    print(f"   🌐 Website: {data.get('website_url', 'N/A')}")
    print(f"   🏷️  Categories: {', '.join(data.get('categories', []))}")
    
    # Check webhook status
    webhook_status = data.get('webhook_status', {})
    if webhook_status.get('status') == 'success':
        print("   ✅ Webhook: Data sent successfully")
    else:
        print(f"   ⚠️  Webhook: {webhook_status.get('message', 'Unknown status')}")

def test_api_endpoints():
    """Test all API endpoints"""
    print("\n🔧 Testing API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print("❌ Health endpoint failed")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test root endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working - Service: {data.get('service', 'Unknown')}")
        else:
            print("❌ Root endpoint failed")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")

def main():
    """Main function"""
    print("🎯 Google Business Scraper - Example Usage")
    print(f"📡 API Base URL: {API_BASE_URL}")
    print("=" * 60)
    
    # Test API endpoints first
    test_api_endpoints()
    
    # Test business extraction
    test_business_extraction()
    
    print("\n" + "=" * 60)
    print("🎉 Example usage completed!")
    print("\n📋 Next steps:")
    print("1. Deploy to Render or Replit")
    print("2. Update API_BASE_URL to your deployed URL")
    print("3. Set up your Zapier webhook")
    print("4. Test with real business data")

if __name__ == "__main__":
    main() 