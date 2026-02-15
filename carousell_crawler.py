from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import time
import json
import random
import re
import os
from database import db
from analysis import text_similarity
from analysis import image_similarity
from analysis import image_similarity2
from utils.logger import get_logger
from utils.driver import create_chrome_driver
from database import schema

logger = get_logger(__name__)


driver = create_chrome_driver(headless=True)
driver.maximize_window()

def write_to_file(crawled_items):
    with open('output.json', 'a', encoding='utf-8') as file:
        json_data = [json.dumps(item, ensure_ascii=False) for item in crawled_items]
        file.write('\n'.join(json_data) + '\n')
    logger.info('saved')

def random_delay(time_start, time_end):
    delay = random.uniform(time_start, time_end)
    time.sleep(delay)

def save_to_db(crawled_item):
    connection = db.get_connection()

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO crawled_items (item_number, seller_name, seller_id, title, description, category, price, images)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    images_json = json.dumps(crawled_item['images'], ensure_ascii=False)
    data = (
        crawled_item['item_number'],
        crawled_item['seller_name'],
        crawled_item['seller_id'],
        crawled_item['title'],
        crawled_item['description'],
        crawled_item['category'],
        crawled_item['price'],
        images_json
    )

    cursor.execute(insert_query, data)
    connection.commit()

    cursor.close()
    
def get_listing_links(driver, num_items=10):
    logger.info("Getting listing links...")

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[starts-with(@data-testid, 'listing-card-')]"))
        )
    except TimeoutException:
        logger.warning("Timeout waiting for listing cards to load.")
        driver.save_screenshot("/app/screenshot_timeout.png")
        return []

    listing_divs = driver.find_elements(By.XPATH, "//div[starts-with(@data-testid, 'listing-card-')]")
    logger.info(f"Found {len(listing_divs)} listing divs")

    result_count = 0
    hrefs = []

    for div in listing_divs:
        try:
            a_tags = div.find_elements(By.TAG_NAME, "a")
            for a in a_tags:
                href = a.get_attribute("href")
                if href and "/p/" in href:
                    hrefs.append(href)
                    result_count += 1
                    break
            if result_count >= num_items:
                break
        except NoSuchElementException:
            continue

    logger.info(f"Collected {len(hrefs)} listing links")
    return hrefs

def get_meta_number(driver):
    try:
        meta_tag = driver.find_element(By.XPATH, '//meta[@name="branch:deeplink:$deeplink_path"]')
        
        content_value = meta_tag.get_attribute('content')
        match = re.search(r'/p/(\d+)', content_value)
        if match:
            number = match.group(1)
            return number
        else:
            logger.info("No number found")
            return None

    except Exception as e:
        logger.info("Error found when get meta number")
        return None

def crawl_listing_page(driver, url):
    driver.get(url)
    time.sleep(3)

    try:
        #wait for load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='new-listing-details-page-desktop-div-seller-contact-header']"))
        )
        number = get_meta_number(driver)
        #get seller content
        seller_container = driver.find_element(By.XPATH, "//div[@data-testid='new-listing-details-page-desktop-div-seller-contact-header']")
        
        #get the user id and name 
        a_tags = seller_container.find_elements(By.TAG_NAME, "a")
        if len(a_tags) >= 2:
            name_id_spans = a_tags[1].find_elements(By.TAG_NAME, "span")
            if len(name_id_spans) >= 2:
                sellername = name_id_spans[0].text
                sellerid = name_id_spans[1].text
            else:
                sellername = "N/A"
                sellerid = "N/A"
        else:
            sellername = "N/A"
            sellerid = "N/A"
            
    except Exception as e:
        logger.info(f"Error: {e}")
        sellername = "N/A"
        sellerid = "N/A"

    try:
        title = driver.find_element(By.XPATH, "//h1[@data-testid='new-listing-details-page-desktop-text-title']").text
    except NoSuchElementException:
        title = ""

    try:
        description = driver.find_element(By.XPATH, "//div[@id='FieldSetField-Container-field_description']//p").text
    except NoSuchElementException:
        description = ""

    try:
        price = driver.find_element(By.XPATH, "//div[@id='FieldSetField-Container-field_price']//h3").text
    except NoSuchElementException:
        price = ""

    try:
        category = driver.find_element(By.XPATH, "//a[starts-with(@href, '/categories/')]/span").text        
    except NoSuchElementException:
        category = ""

    try:
        image_elements = driver.find_elements(By.XPATH, '//div[@id="FieldSetField-Container-field_photo_viewer"]//button//img')
    except NoSuchElementException:
        image_elements = []

    image_urls = []
    for img in image_elements:
        src = img.get_attribute('src')
        if src: 
            image_urls.append(src)
    
    logger.info(f"Item Number: {number}")
    logger.info(f"Title: {title}")
    logger.info(f"Price: {price}")
    logger.info(f"Description: {description}")
    logger.info(f"Category: {category}")
    logger.info(f"Seller Name: {sellername}")
    logger.info(f"Seller ID: {sellerid}")
    
    item = {
        'item_number': number,
        'seller_name': sellername,
        'seller_id': sellerid,
        'title': title,
        'description': description,
        'category': category,
        'price': price,
        'images': image_urls
    }
    
    save_to_db(item)
    
    return item

def main():
    driver.get("https://www.carousell.com.my/") 
    logger.info("Page loaded, sleeping for 5s...")
    time.sleep(5)
    logger.info("Script started1")
    
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(2)

    #find item link
    num_items_to_crawl = 10 #max item count
    logger.info("Script started3")

    listing_links = get_listing_links(driver, num_items=num_items_to_crawl)
    
    logger.info("Script started2")

    crawled_items = []
    logger.info('Crawler running...')
    logger.info("Script started3")

    for link in listing_links:
        logger.info(f'Crawling {link}')
        item = crawl_listing_page(driver, link)
        crawled_items.append(item)
        random_delay(1, 3)
    logger.info('Text similarity running...')
    text_similarity.main()
    logger.info('Image similarity running...')
    image_similarity.main()
    logger.info('Image similarity2 running...')
    image_similarity2.main()
    logger.info('Done')
    driver.quit()

if __name__ == "__main__":
    if os.getenv("RUN_MIGRATIONS", "false").lower() == "true":
        connection = db.get_connection()
        schema.run_migrations(connection)
    main()


