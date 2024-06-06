
import selenium 
import pymongo 
import flask

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random
from pymongo import MongoClient
from datetime import datetime
import uuid

# MongoDB setup
client = MongoClient('localhost', 27017)
db = client.twitter_trends
collection = db.trending_topics

# ProxyMesh setup
PROXY_LIST = [
    "http://proxy1.proxymesh.com:31280",
    "http://proxy2.proxymesh.com:31280",
    # Add more proxies from ProxyMesh as needed
]

def get_random_proxy():
    return random.choice(PROXY_LIST)

# Selenium setup
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")

# Replace with the path to your ChromeDriver
chrome_driver_path = '/path/to/chromedriver'
service = Service(chrome_driver_path)

def fetch_trending_topics():
    # Assign a new proxy for each request
    proxy = get_random_proxy()
    options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get('https://twitter.com/login')
        
        # Log in to Twitter (replace with your credentials)
        username = driver.find_element(By.NAME, "session[username_or_email]")
        password = driver.find_element(By.NAME, "session[password]")
        username.send_keys("your_twitter_username")
        password.send_keys("your_twitter_password")
        password.send_keys(Keys.RETURN)
        
        # Wait for the page to load
        time.sleep(5)
        
        # Fetch trending topics
        trends = driver.find_elements(By.XPATH, '//section[contains(@aria-labelledby, "accessible-list-")]//span')
        trending_topics = [trend.text for trend in trends[:5]]
        
        # Generate a unique ID and get the current date and time
        unique_id = str(uuid.uuid4())
        end_time = datetime.now()
        
        # Store data in MongoDB
        record = {
            "unique_id": unique_id,
            "trend1": trending_topics[0],
            "trend2": trending_topics[1],
            "trend3": trending_topics[2],
            "trend4": trending_topics[3],
            "trend5": trending_topics[4],
            "end_time": end_time,
            "proxy_ip": proxy
        }
        collection.insert_one(record)
        
        return record
        
    finally:
        driver.quit()

# For testing
if __name__ == "__main__":
    result = fetch_trending_topics()
    print(result)
