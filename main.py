from flask import Flask, request, jsonify
from scraper import GoogleBusinessScraper
from utils import clean_text, format_phone_number, format_hours
import json
import requests
import os
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize scraper
scraper = GoogleBusinessScraper()

# Mock Zapier webhook URL (replace with actual webhook URL in production)
ZAPIER_WEBHOOK_URL = os.getenv('ZAPIER_WEBHOOK_URL', 'https://webhook.site/your-unique-url')

@app.route('/extract', methods=['POST'])
def extract_business_data():
    """
    Extract Google Business listing data and send to Zapier webhook
    
    Expected JSON payload:
    {
        "business_name": "Freedom Finders Firm",
        "website_url": "https://freedomfindersfirm.com"  # optional
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No JSON data provided. Please send a JSON object with 'business_name' or 'website_url'."
            }), 400
        
        # Extract business name or URL
        business_name = data.get('business_name', '')
        website_url = data.get('website_url', '')
        
        if not business_name and not website_url:
            return jsonify({
                "error": "Please provide either 'business_name' or 'website_url' in the request body."
            }), 400
        
        # Use website URL if provided, otherwise use business name
        search_input = website_url if website_url else business_name
        
        # Extract business data
        result = scraper.get_business_data(search_input)
        
        # Check if extraction was successful
        if 'error' in result:
            return jsonify(result), 404
        
        # Send data to Zapier webhook (mock for now)
        webhook_result = send_to_zapier(result)
        
        # Add webhook status to response
        result['webhook_status'] = webhook_result
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Google Business Scraper",
        "version": "1.0.0"
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with usage instructions"""
    return jsonify({
        "service": "Google Business Listing Scraper",
        "version": "1.0.0",
        "usage": {
            "endpoint": "/extract",
            "method": "POST",
            "content_type": "application/json",
            "example_payload": {
                "business_name": "Freedom Finders Firm",
                "website_url": "https://freedomfindersfirm.com"
            }
        },
        "endpoints": {
            "/extract": "Extract business data and send to webhook",
            "/health": "Health check",
            "/": "This help message"
        }
    }), 200

def send_to_zapier(data):
    """Send extracted data to Zapier webhook"""
    try:
        # Prepare the payload for Zapier
        webhook_payload = {
            "source": "google_business_scraper",
            "timestamp": str(datetime.datetime.now()),
            "business_data": data
        }
        
        # Send POST request to Zapier webhook
        response = requests.post(
            ZAPIER_WEBHOOK_URL,
            json=webhook_payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code in [200, 201, 202]:
            return {
                "status": "success",
                "message": "Data sent to Zapier webhook successfully",
                "webhook_response": response.text
            }
        else:
            return {
                "status": "error",
                "message": f"Webhook request failed with status {response.status_code}",
                "webhook_response": response.text
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Failed to send to webhook: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error sending to webhook: {str(e)}"
        }

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found. Use /extract for business data extraction."
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error. Please try again later."
    }), 500

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
else:
    # For production (Render, Replit, etc.)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 