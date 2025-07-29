import requests
import re
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from utils import clean_text, extract_rating, extract_reviews, extract_categories

class GoogleBusinessScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_business_data(self, business_name_or_url):
        """Main function to extract business data from Google"""
        try:
            # Determine if input is URL or business name
            if business_name_or_url.startswith(('http://', 'https://')):
                # Extract domain and search for it
                domain = self._extract_domain(business_name_or_url)
                search_query = domain
            else:
                search_query = business_name_or_url
            
            # Try different search strategies
            data = self._search_google_maps(search_query)
            if not data:
                data = self._search_google_search(search_query)
            
            if data:
                return self._format_response(data)
            else:
                return {"error": "Business listing not found. Please verify the name or try again."}
                
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
    
    def _extract_domain(self, url):
        """Extract domain from URL"""
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        return domain
    
    def _search_google_maps(self, query):
        """Search Google Maps for business listing"""
        try:
            # Format query for Google Maps search
            search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
            
            # Use Selenium for Google Maps (more reliable)
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(f'--user-agent={self.ua.random}')
            
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            driver.get(search_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Try to find business listing
            try:
                # Look for business name
                business_name = driver.find_element(By.CSS_SELECTOR, 'h1, .fontHeadlineLarge').text
                
                # Extract rating
                rating_element = driver.find_element(By.CSS_SELECTOR, '[aria-label*="stars"], .fontDisplayLarge')
                rating = extract_rating(rating_element.text)
                
                # Extract review count
                review_count = 0
                try:
                    review_element = driver.find_element(By.CSS_SELECTOR, '[aria-label*="reviews"]')
                    review_count = int(re.findall(r'\d+', review_element.text)[0])
                except:
                    pass
                
                # Extract address
                address = ""
                try:
                    address_element = driver.find_element(By.CSS_SELECTOR, '[data-item-id*="address"]')
                    address = clean_text(address_element.text)
                except:
                    pass
                
                # Extract phone
                phone = ""
                try:
                    phone_element = driver.find_element(By.CSS_SELECTOR, '[data-item-id*="phone"]')
                    phone = clean_text(phone_element.text)
                except:
                    pass
                
                # Extract website
                website = ""
                try:
                    website_element = driver.find_element(By.CSS_SELECTOR, '[data-item-id*="authority"]')
                    website = website_element.get_attribute('href')
                except:
                    pass
                
                # Extract hours
                hours = ""
                try:
                    hours_element = driver.find_element(By.CSS_SELECTOR, '[data-item-id*="hours"]')
                    hours = clean_text(hours_element.text)
                except:
                    pass
                
                # Extract categories
                categories = []
                try:
                    category_elements = driver.find_elements(By.CSS_SELECTOR, '[data-item-id*="category"]')
                    categories = [clean_text(elem.text) for elem in category_elements]
                except:
                    pass
                
                # Extract reviews
                reviews = extract_reviews(driver)
                
                # Get Google Maps link
                maps_link = driver.current_url
                
                driver.quit()
                
                return {
                    'business_name': business_name,
                    'star_rating': rating,
                    'review_count': review_count,
                    'address': address,
                    'phone_number': phone,
                    'website_url': website,
                    'hours_of_operation': hours,
                    'categories': categories,
                    'top_reviews': reviews,
                    'google_maps_link': maps_link
                }
                
            except Exception as e:
                driver.quit()
                return None
                
        except Exception as e:
            return None
    
    def _search_google_search(self, query):
        """Search Google Search for business listing"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}+google+business"
            
            response = self.session.get(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for Google Business listing in search results
            business_data = {}
            
            # Try to find business name
            name_selectors = ['h3', '.LC20lb', '.r']
            for selector in name_selectors:
                name_elem = soup.select_one(selector)
                if name_elem:
                    business_data['business_name'] = clean_text(name_elem.text)
                    break
            
            # Try to find rating
            rating_elem = soup.select_one('[aria-label*="stars"]')
            if rating_elem:
                business_data['star_rating'] = extract_rating(rating_elem.get('aria-label', ''))
            
            # Try to find review count
            review_elem = soup.select_one('[aria-label*="reviews"]')
            if review_elem:
                review_text = review_elem.get('aria-label', '')
                review_count = re.findall(r'\d+', review_text)
                if review_count:
                    business_data['review_count'] = int(review_count[0])
            
            # Try to find address
            address_elem = soup.select_one('.adr, [data-ved*="address"]')
            if address_elem:
                business_data['address'] = clean_text(address_elem.text)
            
            # Try to find phone
            phone_elem = soup.select_one('[data-ved*="phone"]')
            if phone_elem:
                business_data['phone_number'] = clean_text(phone_elem.text)
            
            # Try to find website
            website_elem = soup.select_one('a[href*="http"]')
            if website_elem:
                business_data['website_url'] = website_elem.get('href')
            
            if business_data.get('business_name'):
                return business_data
            
            return None
            
        except Exception as e:
            return None
    
    def _format_response(self, data):
        """Format the scraped data into the required JSON structure"""
        return {
            "business_name": data.get('business_name', ''),
            "star_rating": data.get('star_rating', ''),
            "review_count": data.get('review_count', 0),
            "top_reviews": data.get('top_reviews', []),
            "categories": data.get('categories', []),
            "hours_of_operation": data.get('hours_of_operation', ''),
            "address": data.get('address', ''),
            "website_url": data.get('website_url', ''),
            "phone_number": data.get('phone_number', ''),
            "profile_photo_url": data.get('profile_photo_url', ''),
            "services_listed": data.get('services_listed', []),
            "business_attributes": data.get('business_attributes', []),
            "google_maps_link": data.get('google_maps_link', '')
        } 