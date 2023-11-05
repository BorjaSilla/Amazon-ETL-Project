import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import re
import os

def scrape_amazon_url(url, num_pages):

    counter = 1
    # Extract the category name from the URL
    category_name = re.search(r'/bestsellers/([^/]+)/', url).group(1)
    # Create the directory if it doesn't exist one level up
    csv_filename = f'scrape_data/{category_name}_top100.csv'


    # Start a driver instance
    driver = webdriver.Chrome()
    driver.get(url)

    # Create a CSV file and write the header only once
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['rank', 'asin', 'title', 'price', 'rating', 'num_reviews', 'img_link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for page in range(num_pages):
        time.sleep(2)  # Add a delay if needed

        # Close cookies popup - if needed
        try:
            driver.find_element(By.XPATH, '//*[@id="sp-cc-accept"]').click()
            print('Cookies Accepted, starting scrape...')
            print(f'Scraping {category_name} Top 100 ----------------------------------------- page: {counter}')
            time.sleep(1)
        except:
            print("Cookies not needed")
            print(f'Scraping {category_name} Top 100 ----------------------------------------- page: {counter}')

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)  # Increase the sleep duration to 4 seconds (or adjust as needed)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


        # Find product container and save it
        caja_productos = driver.find_elements(By.CLASS_NAME, 'a-cardui._cDEzb_grid-cell_1uMOS.expandableGrid.p13n-grid-content')

        # Data Extraction
        rank = [int(i.text.split('\n')[0].split('#')[1]) for i in caja_productos]
        print(rank)
        titulos = [i.text.split('\n')[1] for i in caja_productos]
        print(titulos)

        precio = []
        ratings = []
        ratings_float = []
        num_reviews = []  

        for item in caja_productos:
            item_text = item.text.split('\n')

            # Check if the item has the expected number of elements
            if len(item_text) >= 4:
                review_text = item_text[3]  # Extract the review text

                if review_text.strip():  # Check if the review text is not empty
                    numeric_review = re.sub(r'[^\d]', '', review_text)  # Remove non-numeric characters
                    if numeric_review:  # Check if the cleaned string is not empty
                        num_reviews.append(int(numeric_review))  # Convert the cleaned string to an integer
                    else:
                        num_reviews.append(0)  # Set a default value to indicate no reviews
                else:
                    num_reviews.append(0)  # If the review text is empty, set the number of reviews to 0
            else:
                num_reviews.append(0)  # Handle cases where the item doesn't have the expected structure


        for e in caja_productos:
            try:
                precio_text = e.text.split('\n')[4]
                precio_value = float(precio_text.split()[0].replace(',', '.'))
                precio.append(precio_value)
            except:
                precio.append(0)


        for product in caja_productos:
            try:
                rating_element = product.find_element(By.CSS_SELECTOR, "i.a-icon-star-small span.a-icon-alt")
                rating_text = rating_element.get_attribute("textContent")
                if rating_text.strip():
                    rating = rating_text.split(" de ")[0]
                else:
                    rating = '0'
            except:
                rating = '0'
            
            ratings.append(rating)
            rating_value = rating.replace(',', '.').strip()
            ratings_float.append(float(rating_value))


        # IMAGE EXTRACTION

        image_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-asin] a.a-link-normal img.a-dynamic-image")
        image_links = [image.get_attribute("src") for image in image_elements]

        # ASIN EXTRACTION

        asin_elements = driver.find_elements(By.XPATH, '//div[@data-asin]')
        asin = [i.get_attribute('data-asin') for i in asin_elements]

        # CHECK LEN OF EXTRACTED VALUES (SHOULD = 50)
        print('rank', len(rank), 'asin', len(asin), 'title', len(titulos), 'precio', len(precio), 'ratings', len(ratings), 'num_reviews', len(num_reviews), 'image links', len(image_links))

        # Create a list of dictionaries for the current page's data
        page_data = [
            {
                'rank': r,
                'asin' : a,
                'title': t,
                'price': p,
                'rating': rt,
                'num_reviews': nr,
                'img_link': il
            }
            for r, a, t, p, rt, nr, il in zip(rank, asin, titulos, precio, ratings_float, num_reviews, image_links)
        ]

        # Append data to the CSV file
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(page_data)


        # Step 6: Click on the element to navigate to the next page
        try:
            next_page_element = driver.find_element(By.CSS_SELECTOR, 'div.a-cardui._cDEzb_card_1L-Yx > div.a-text-center > ul > li.a-last')
            next_page_element.click()
            counter += 1
        except:
            print(f"Failed to navigate to page {page + 1}")
        
            
    # Close the web driver when you're done with all pages
    print("Scraping done, closing window")
    driver.quit()