import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import re

def scrape_amazon_url(url, num_pages):
    # Extract the category name from the URL
    category_name = re.search(r'/bestsellers/([^/]+)/', url).group(1)
    # Create the CSV filename with the category name
    csv_filename = f'../scrape_data/{category_name}_top100.csv'

    # Start a driver instance
    driver = webdriver.Chrome()
    driver.get(url)

    # Create a CSV file and write the header only once
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['rank', 'title', 'price', 'rating', 'num_reviews', 'img_link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for page in range(num_pages):
        time.sleep(2)  # Add a delay if needed

        # Close cookies popup - if needed
        try:
            driver.find_element(By.XPATH, '//*[@id="sp-cc-accept"]').click()
            time.sleep(1)
        except:
            print("Cookies not needed")

        # Scroll to the end of the website to load all elements
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Find product container and save it
        caja_productos = driver.find_elements(By.CLASS_NAME, 'a-cardui._cDEzb_grid-cell_1uMOS.expandableGrid.p13n-grid-content')

        # Data Extraction
        rank = [int(i.text.split('\n')[0].split('#')[1]) for i in caja_productos]
        titulos = [i.text.split('\n')[1] for i in caja_productos]
        precio = []
        num_reviews = [int(i.text.split('\n')[2].replace('.', '')) for i in caja_productos]

        for e in caja_productos:
            try:
                precio_text = e.text.split('\n')[3]
                precio_value = float(precio_text.split()[0].replace(',', '.'))
                precio.append(precio_value)
            except:
                precio.append(0)

        rating_elements = driver.find_elements(By.CSS_SELECTOR, "i.a-icon-star-small span.a-icon-alt")
        ratings = [rating.get_attribute("textContent").split(" de ")[0] for rating in rating_elements]
        ratings_float = [float(rating.replace(',', '.').strip()) for rating in ratings]

        image_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-asin] a.a-link-normal img.a-dynamic-image")
        image_links = [image.get_attribute("src") for image in image_elements]

        # Create a list of dictionaries for the current page's data
        page_data = [
            {
                'rank': r,
                'title': t,
                'price': p,
                'rating': rt,
                'num_reviews': nr,
                'img_link': il
            }
            for r, t, p, rt, nr, il in zip(rank, titulos, precio, ratings_float, num_reviews, image_links)
        ]

        # Append data to the CSV file
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(page_data)

        # Step 6: Click on the element to navigate to the next page
        try:
            next_page_element = driver.find_element(By.CSS_SELECTOR, 'div.a-cardui._cDEzb_card_1L-Yx > div.a-text-center > ul > li.a-last')
            next_page_element.click()
        except:
            print(f"Failed to navigate to page {page + 1}")

    # Close the web driver when you're done with all pages
    driver.quit()

    scrape_amazon_url('https://www.amazon.es/gp/bestsellers/music/ref=zg_bs_nav_music_0', 2)