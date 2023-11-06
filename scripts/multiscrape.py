import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import re
import os
import multiprocessing
from scrape_links import links
from scrape import scrape_amazon_url


# Function to scrape a single link
def scrape_single_link(link):
    # Modify this function to call scrape_amazon_url for a single link
    # You can add error handling or logging as needed
    try:
        scrape_amazon_url(link, 2)  # You can specify the number of pages here
    except Exception as e:
        print(f"Error scraping {link}: {str(e)}")

if __name__ == '__main__':
    # Number of processes to create (you can adjust this as needed)
    num_processes = 3

    # Create a multiprocessing pool to run the scraping function in parallel
    with multiprocessing.Pool(num_processes) as pool:
        pool.map(scrape_single_link, links)