import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from IPython.display import Markdown
# Set up Chrome options to bypass bot detection
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--incognito")  # Incognito mode
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open Amazon
query = "laptop"
url = f"https://www.amazon.in/s?k={query}"
driver.get(url)

# Wait for the page to load
time.sleep(random.uniform(3, 6))

# Prepare CSV file
csv_filename = "amazon_products.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating"])  # Header

    products_collected = 0
    max_products = 100  # Target number of products
    max_pages = 10  # Scrape up to 10 pages

    for page in range(1, max_pages + 1):
        print(f"📄 Scraping Page {page}...")

        # Extract product details
        elements = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

        for elem in elements:
            if products_collected >= max_products:
                break  # Stop if we reach the target number

            try:
                title = elem.find_element(By.TAG_NAME, "h2").text
            except:
                title = "N/A"

            try:
                price = elem.find_element(By.CLASS_NAME, "a-price-whole").text
            except:
                price = "N/A"

            try:
                rating = elem.find_element(By.CLASS_NAME, "a-icon-alt").text
            except:
                rating = "N/A"

            writer.writerow([title, price, rating])
            products_collected += 1

        # Try to go to the next page
        try:
            next_button = driver.find_element(By.XPATH, "//a[contains(@class, 's-pagination-next')]")
            if "disabled" in next_button.get_attribute("class"):
                print("🚨 No more pages available.")
                break  # Exit loop if no more pages
            next_button.click()
            time.sleep(random.uniform(5, 8))  # Random delay to mimic human behavior
        except:
            print("⚠️ Could not find Next Page button. Exiting...")
            break

print(f"✅ Successfully saved {products_collected} products to {csv_filename}!")
driver.quit()