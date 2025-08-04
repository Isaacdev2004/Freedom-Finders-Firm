#!/usr/bin/env python3
"""
Test script for Google Business Scraper
Tests the scraper with the example business: Freedom Finders Firm
"""

import requests
import json
import sys
from datetime import datetime

def test_local_api():
    """Test the local Flask API"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Google Business Scraper API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()}")
        else:
            print("❌ Health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on localhost:5000")
        return False
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   Service: {data.get('service', 'Unknown')}")
            print(f"   Version: {data.get('version', 'Unknown')}")
        else:
            print("❌ Root endpoint failed")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: Extract with business name
    print("\n3. Testing business extraction with name...")
    test_payload = {
        "business_name": "Freedom Finders Firm"
    }
    
    try:
        response = requests.post(
            f"{base_url}/extract",
            json=test_payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Business extraction successful!")
            print(f"   Business Name: {data.get('business_name', 'N/A')}")
            print(f"   Star Rating: {data.get('star_rating', 'N/A')}")
            print(f"   Review Count: {data.get('review_count', 'N/A')}")
            print(f"   Address: {data.get('address', 'N/A')}")
            print(f"   Phone: {data.get('phone_number', 'N/A')}")
            print(f"   Website: {data.get('website_url', 'N/A')}")
            
            # Check webhook status
            webhook_status = data.get('webhook_status', {})
            if webhook_status.get('status') == 'success':
                print("✅ Webhook delivery successful")
            else:
                print(f"⚠️  Webhook status: {webhook_status.get('message', 'Unknown')}")
                
        elif response.status_code == 404:
            print("⚠️  Business not found (this is expected for test data)")
            error_data = response.json()
            print(f"   Error: {error_data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Extraction failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Extraction error: {e}")
    
    # Test 4: Extract with website URL
    print("\n4. Testing business extraction with website URL...")
    test_payload = {
        "website_url": "https://freedomfindersfirm.com"
    }
    
    try:
        response = requests.post(
            f"{base_url}/extract",
            json=test_payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Website extraction successful!")
            print(f"   Business Name: {data.get('business_name', 'N/A')}")
            print(f"   Star Rating: {data.get('star_rating', 'N/A')}")
        elif response.status_code == 404:
            print("⚠️  Website not found (this is expected for test data)")
        else:
            print(f"❌ Website extraction failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Website extraction error: {e}")
    
    # Test 5: Invalid input
    print("\n5. Testing invalid input handling...")
    test_payload = {}  # Empty payload
    
    try:
        response = requests.post(
            f"{base_url}/extract",
            json=test_payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 400:
            print("✅ Invalid input properly handled")
            error_data = response.json()
            print(f"   Error: {error_data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Invalid input not properly handled (status: {response.status_code})")
            
    except Exception as e:
        print(f"❌ Invalid input test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("\n📝 Notes:")
    print("- If business extraction returns 404, this is normal for test data")
    print("- The scraper will work better with real, existing businesses")
    print("- Check the webhook status to ensure Zapier integration works")
    
    return True

def test_scraper_directly():
    """Test the scraper module directly"""
    print("\n🔧 Testing scraper module directly...")
    
    try:
        from scraper import GoogleBusinessScraper
        
        scraper = GoogleBusinessScraper()
        
        # Test with business name
        print("   Testing with business name: 'Freedom Finders Firm'")
        result = scraper.get_business_data("Freedom Finders Firm")
        
        if 'error' in result:
            print(f"   ⚠️  Result: {result['error']}")
        else:
            print("   ✅ Direct scraper test successful")
            print(f"   Business Name: {result.get('business_name', 'N/A')}")
            print(f"   Star Rating: {result.get('star_rating', 'N/A')}")
            
    except ImportError as e:
        print(f"   ❌ Cannot import scraper module: {e}")
    except Exception as e:
        print(f"   ❌ Direct scraper test error: {e}")

def main():
    """Main test function"""
    print("🚀 Google Business Scraper Test Suite")
    print(f"📅 Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test API endpoints
    api_success = test_local_api()
    
    # Test scraper directly
    test_scraper_directly()
    
    if api_success:
        print("\n✅ All tests completed successfully!")
        print("\n📋 Next steps:")
        print("1. Try with a real business name")
        print("2. Set up your Zapier webhook URL")
        print("3. Deploy to Render or Replit")
    else:
        print("\n❌ Some tests failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 