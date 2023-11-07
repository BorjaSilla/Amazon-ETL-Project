![ETL](https://www.infobelpro.com/hs-fs/hubfs/ETL.png?width=840&height=420&name=ETL.png)

# Amazon Web Scraping and ETL Project

This project involves scraping data from Amazon's product listings, using Selenium for web scraping, and applying multiprocessing to speed up data extraction. After scraping, the data is cleaned and immediately stored in CSV files. The project's primary steps are as follows:

## Project Structure

- `scrape.py`: Python script for web scraping using Selenium.
- `scrape_links.py`: Script for extraction of the links of all the categorie's top 100 products.
- `multiscrape.py`: The multiprocessing version to scrape more efficiently with parallel processes.
- `scrape_data`: A folder containing scraped data per category in `CSV` format.
- `README.md`: Project documentation (this file).


## Project Steps

### 1. URL Extraction

- Extracting a list of URLs for the top 100 pages of Amazon categories.

### 2. Web Scraping with Selenium and Multiprocessing

- The `multiscrape.py` script uses Selenium to automate web interactions and multiprocessing for concurrent scraping.
- It opens multiple browser instances to scrape data simultaneously.
- The script navigates the Amazon website, scrolls down, clicks "Load More" buttons, and extracts data from various pages.
- The data is stored in `CSV` data structures.

### 3. Real-time Data Cleaning

- The `multiscrape.py` script contains functions for immediate data cleaning as it is scraped.
- Data cleaning includes handling missing values, removing duplicates, correcting formatting issues, and structuring the data as needed.

### 4. Storing Data in CSV Files

- CSV files are created to store the cleaned data with a format string to save the file with the name of the category.
- Each CSV file may represent data from a specific Amazon category.
- The cleaned data is written to the CSV files using Python's CSV-writing libraries.

### 5. Further Steps

- With the data now in CSV files, I proceeded to enrinch the data with a dataset.

#### Example Further Steps:

- **Data Analysis**: Utilize data analysis tools like Pandas and Jupyter to gain insights from the data.
- **Machine Learning**: Explore machine learning models for predictions based on the Amazon data.
- **Scheduled Updates**: Implement a scheduler for periodic data re-scraping to keep the dataset up-to-date.
- **API Development**: Create an API to expose the data for external applications or integration with other services.
- **Data Export**: Consider exporting the data to databases, data lakes, or cloud storage for long-term storage and scalability.

Remember to document your work thoroughly, including your scraping and data cleaning code. Ensure compliance with web scraping ethics and respect Amazon's terms of service to avoid any legal issues.
