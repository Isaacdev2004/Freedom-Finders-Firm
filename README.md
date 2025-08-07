# Google Business Listing Scraper

A standalone Flask backend tool that extracts public Google Business listing data and sends it to a Zapier webhook for further processing with OpenAI.

## 🚀 Features

- **Business Data Extraction**: Scrapes Google Maps and Google Search for business listings
- **Flexible Input**: Accepts business names or website URLs
- **Structured JSON Output**: Returns clean, formatted business data
- **Zapier Integration**: Sends extracted data to webhook for automation
- **Error Handling**: Graceful handling of missing listings and scraping errors
- **Production Ready**: Deployable on Render, Replit, or any Python hosting platform

## 📊 Data Fields Extracted

- `business_name`: Company name
- `star_rating`: Average star rating (0-5)
- `review_count`: Number of reviews
- `top_reviews`: First 3-5 reviews with star ratings and text
- `categories`: Business categories (e.g., "Consulting", "Marketing Agency")
- `hours_of_operation`: Operating hours
- `address`: Physical address
- `website_url`: Company website
- `phone_number`: Contact phone number
- `profile_photo_url`: Business profile image (if available)
- `services_listed`: Services offered (if available)
- `business_attributes`: Special attributes (e.g., "Black-owned", "Women-led")
- `google_maps_link`: Direct link to Google Maps listing

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.8+
- Chrome browser (for Selenium webdriver)

### Local Development

1. **Clone or create the project**:
   ```bash
   mkdir google-business-scraper
   cd google-business-scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional):
   ```bash
   # Create .env file
   echo "ZAPIER_WEBHOOK_URL=https://webhook.site/your-unique-url" > .env
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

The server will start on `http://localhost:5000`

## 📡 API Usage

### Extract Business Data

**Endpoint**: `POST /extract`

**Request Body**:
```json
{
  "business_name": "Freedom Finders Firm"
}
```

OR

```json
{
  "website_url": "https://freedomfindersfirm.com"
}
```

OR (for Zapier integration):

```json
{
  "business_name": "Freedom Finders Firm",
  "return_webhook_url": "https://hooks.zapier.com/your-return-webhook"
}
```

**Response Example**:
```json
{
  "business_name": "Freedom Finders Firm",
  "star_rating": "4.6",
  "review_count": 52,
  "top_reviews": [
    {"stars": 5, "text": "Excellent team and very professional service."},
    {"stars": 4, "text": "Great experience working with this company."}
  ],
  "categories": ["Consulting", "Business Services"],
  "hours_of_operation": "Mon-Fri 9am–5pm",
  "address": "123 Business St, New York, NY",
  "website_url": "https://freedomfindersfirm.com",
  "phone_number": "(123) 456-7890",
  "profile_photo_url": "https://example.com/logo.jpg",
  "services_listed": ["Tax Consulting", "Business Planning"],
  "business_attributes": ["Black-owned", "Women-led"],
  "google_maps_link": "https://maps.google.com/?q=Freedom+Finders+Firm",
  "webhook_status": {
    "status": "success",
    "message": "Data sent to Zapier webhook successfully"
  }
}
```

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "service": "Google Business Scraper",
  "version": "1.0.0"
}
```

### Root Endpoint

**Endpoint**: `GET /`

Returns API usage information and available endpoints.

## 🧪 Testing

### Using curl

```bash
# Test with business name
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"business_name": "Freedom Finders Firm"}'

# Test with website URL
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"website_url": "https://freedomfindersfirm.com"}'
```

### Using Python requests

```python
import requests

# Test the API
response = requests.post(
    'http://localhost:5000/extract',
    json={'business_name': 'Freedom Finders Firm'},
    headers={'Content-Type': 'application/json'}
)

print(response.json())
```

## 🚀 Deployment

### Render Deployment

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn main:app`

3. **Add environment variables**:
   - `ZAPIER_WEBHOOK_URL`: Your Zapier webhook URL

4. **Deploy** and get your live URL

### Replit Deployment

1. **Create a new Repl** at [replit.com](https://replit.com)
2. **Upload your files** or connect to GitHub
3. **Set environment variables** in the Secrets tab
4. **Run** the application

### Environment Variables

- `ZAPIER_WEBHOOK_URL`: Your Zapier webhook URL (optional, defaults to mock URL)
- `PORT`: Port number (optional, defaults to 5000)

## 🔧 Configuration

### Zapier Webhook Setup

1. **Create a Zapier account** at [zapier.com](https://zapier.com)
2. **Create a new Zap** with "Webhook" as trigger
3. **Copy the webhook URL** and set it as `ZAPIER_WEBHOOK_URL`
4. **Configure actions** to send data to OpenAI or other services

### Customizing Scraping

Edit `scraper.py` to modify:
- Search strategies
- Data extraction patterns
- User agent rotation
- Error handling

## 🛡️ Error Handling

The application handles various error scenarios:

- **Business not found**: Returns 404 with error message
- **Invalid input**: Returns 400 with validation error
- **Scraping failures**: Returns 500 with error details
- **Webhook failures**: Continues but reports webhook status

## 📁 Project Structure

```
google-business-scraper/
├── main.py              # Flask application
├── scraper.py           # Google scraping logic
├── utils.py             # Helper functions
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .env               # Environment variables (optional)
```

## 🔍 How It Works

1. **Input Processing**: Accepts business name or website URL
2. **Google Search**: Searches Google Maps and Google Search
3. **Data Extraction**: Uses Selenium and BeautifulSoup to extract data
4. **Data Cleaning**: Formats and validates extracted data
5. **Webhook Delivery**: Sends structured JSON to Zapier
6. **Response**: Returns formatted data with webhook status

## ⚠️ Important Notes

- **Rate Limiting**: Be respectful of Google's servers
- **Terms of Service**: Only scrape public data
- **User Agents**: Rotates user agents to avoid detection
- **Error Recovery**: Graceful handling of scraping failures
- **Data Accuracy**: Results may vary based on listing availability

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and business use. Please respect Google's terms of service when scraping data.

## 🆘 Support

For issues or questions:
1. Check the error handling section
2. Review the API documentation
3. Test with the provided examples
4. Check deployment logs for errors 