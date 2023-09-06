import numpy as np
import requests
from bs4 import BeautifulSoup, ResultSet
import pandas as pd

if __name__ == '__main__':
    # Define user-agent and language headers for the HTTP requests
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/16.6 Safari/605.1.15',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    # Create an empty list to store href tags
    href_tags = []

    # Initialize variables for web scraping
    soup = None
    webpage = None
    new_webpage = None
    new_soup = None
    new_URL = None

    # Create a dictionary to store product information
    d = {'product_name': [], 'product_price': [], 'product_rating': [], 'review_cnt': [], 'availability': []}


    # Define functions to extract product information

    def get_product_name(webpage_content):
        try:
            product_name = (webpage_content
                            .find('span', attrs={'id': 'productTitle'})
                            .text
                            .strip())
        except AttributeError:
            product_name = ''
        return product_name


    def get_product_price(webpage_content):
        try:
            product_price = (webpage_content.find('div', attrs={'class': 'a-section a-spacing-none aok-align-center'})
                             .find('span', attrs={'class': 'a-price-whole'}).text)
        except AttributeError:
            product_price = ''
        return product_price


    def get_product_rating(webpage_content):
        try:
            product_rating = (webpage_content
                              .find('div', attrs={'id': 'averageCustomerReviews'})
                              .find('span', attrs={'class': 'a-size-base a-color-base'})
                              .text
                              .strip())
        except AttributeError:
            product_rating = ''
        return product_rating


    def get_review_cnt(webpage_content):
        try:
            review_cnt = (webpage_content
            .find('a', attrs={'id': 'acrCustomerReviewLink'})
            .find('span', attrs={'id': 'acrCustomerReviewText'})
            .text
            .split()[0])
        except AttributeError:
            review_cnt = ''
        return review_cnt


    def get_availability(webpage_content):
        try:
            availability = (webpage_content
                            .find('div', attrs={'id': 'availabilityInsideBuyBox_feature_div'})
                            .find('div', attrs={'id': 'availability'})
                            .text
                            .strip())
        except AttributeError:
            availability = ''
        return availability


    # Loop through pages for web scraping
    for i in range(1, 10):
        try:
            # Send an HTTP GET request to the Amazon search page
            webpage = requests.get(
                f'https://www.amazon.in/s?k=playstation+5&i=videogames&rh=n%3A976460031%2Cp_89%3ASony&dc&page={i}&crid=112WNC5PLHFK0&qid=1693712700&rnid=3837712031&sprefix=%2Caps%2C288&ref=sr_pg_{i}',
                headers=HEADERS)
            webpage.raise_for_status()  # Raise an exception if the request was not successful
        except Exception as e:
            print(e)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(webpage.content, 'html.parser')

        # Find all elements containing href tags
        tags: ResultSet = soup.find_all('a', attrs={
            'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

        # Append href tags to the list
        for tag in tags:
            href_tags.append(tag.get('href'))

    # Iterate through href tags to scrape product information
    for tag in href_tags:
        new_URL = 'https://amazon.in' + tag
        new_webpage = requests.get(new_URL, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

        # Extract product information and append to the dictionary
        d['product_name'].append(get_product_name(new_soup))
        d['product_price'].append(get_product_price(new_soup))
        d['product_rating'].append(get_product_rating(new_soup))
        d['review_cnt'].append(get_review_cnt(new_soup))
        d['availability'].append(get_availability(new_soup))

    # Create a pandas DataFrame from the collected product information
    amazon_data_df = pd.DataFrame.from_dict(d)

    # Replace empty product names with NaN and drop rows with NaN product names
    amazon_data_df['product_name'].replace('', np.NaN, inplace=True)
    amazon_data_df = amazon_data_df.dropna(subset=['product_name'])

    # Save the DataFrame to a CSV file
    amazon_data_df.to_csv('./output_files/amazon_multiple_pages_data.csv')
