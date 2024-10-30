import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Checking
print("Script started...")
print("Webhook URL:", DISCORD_WEBHOOK_URL)

CHECK_INTERVAL = 3600  # Check every hour
URL = 'https://www.matchajp.net/collections/500g'

def check_stock():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Adjust the selector based on the HTML structure of the website
    product_cards = soup.select('div.product-card')  # Update with actual class name

    in_stock = False
    for product in product_cards:
        if "Sold Out" not in product.get_text():
            in_stock = True
            product_name = product.find('a', {'class': 'product-title'}).text
            notify_user(product_name)
            break

    if not in_stock:
        print("All products are still sold out.")

def notify_user(product_name):
    message = {
        "content": f"Product Alert: {product_name} is back in stock! Check it out here: {URL}"
    }
    
    # Send a POST request to the Discord webhook
    response = requests.post(DISCORD_WEBHOOK_URL, json=message)
    
    # Check for errors
    if response.status_code == 204:
        print(f"Notification sent for {product_name}")
    else:
        print(f"Failed to send notification: {response.status_code}")

if __name__ == "__main__":
    while True:
        check_stock()
        time.sleep(CHECK_INTERVAL)
