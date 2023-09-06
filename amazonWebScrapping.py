import numpy as np
import requests
from bs4 import BeautifulSoup, ResultSet
import pandas as pd

if __name__ == '__main__':
    # Define the URL and headers for the Amazon product search page
    URL = 'https://www.amazon.in/s?k=playstation+5&crid=1MPMPYIDNS00Z&sprefix=playstation+5%2Caps%2C238&ref=nb_sb_noss_1'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/16.6 Safari/605.1.15',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    # Send an HTTP request to the Amazon product search page
    webpage = requests.get(URL, headers=HEADERS)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(webpage.content, 'html.parser')

    # Find all the links on the page with specific attributes
    links: ResultSet = soup.find_all('a', attrs={
        'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    # Create an empty list to store extracted links
    links_list = []
    for link in links:
        links_list.append(link.get('href'))


    # Function to get the product name from a BeautifulSoup object
    def get_product_name(soup_info):
        try:
            product_title = (soup_info.find('span', attrs={'id': 'productTitle'}))
            title_value = product_title.string
            title_string = title_value.strip()
        except AttributeError:
            title_string = ''
        return title_string


    # Function to get the product price from a BeautifulSoup object
    def get_product_price(soup_info):
        try:
            product_price = soup_info.find('span', attrs={
                'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
            product_value = product_price.find('span', attrs={'class': 'a-price-whole'}).string
        except AttributeError:
            product_value = ''
        return product_value


    # Function to get the product rating from a BeautifulSoup object
    def get_product_rating(soup_info):
        try:
            product_rating = soup_info.find('div', attrs={'id': 'averageCustomerReviews'})
            prd_rating_value = (product_rating
                                .find('span', attrs={'class': 'a-size-base a-color-base'})
                                .string
                                .strip())
        except AttributeError:
            prd_rating_value = ''
        return prd_rating_value


    # Function to get the review count from a BeautifulSoup object
    def get_review_count(soup_info):
        try:
            review_count = soup_info.find('div', attrs={'class': 'a-row a-spacing-medium averageStarRatingNumerical'})
            review_count_val = (review_count
                                .find('span', attrs={'class': 'a-size-base a-color-secondary'})
                                .string
                                .strip())
        except AttributeError:
            review_count_val = ''
        return review_count_val


    # Function to get the product availability from a BeautifulSoup object
    def get_product_availability(soup_info):
        try:
            product_availability = soup_info.find('div', attrs={'id': 'availability'})
            product_availability_value = (product_availability
                                          .find('span', attrs={'class': 'a-size-medium a-color-success'})
                                          .string.strip())
        except AttributeError:
            product_availability_value = ''
        return product_availability_value


    # Create a dictionary to store product information
    d = {'product_name': [], 'product_price': [], 'product_rating': [], 'review_cnt': [], 'availability': []}

    # Iterate through the extracted links to gather product information
    for link in links_list:
        new_url = 'https://amazon.in' + link
        new_webpage = requests.get(new_url, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, 'html.parser')
        d['product_name'].append(get_product_name(new_soup))
        d['product_price'].append(get_product_price(new_soup))
        d['product_rating'].append(get_product_rating(new_soup))
        d['review_cnt'].append(get_review_count(new_soup))
        d['availability'].append(get_product_availability(new_soup))

    # Create a pandas DataFrame from the collected data
    amazon_df = pd.DataFrame.from_dict(d)

    # Replace empty product names with NaN and drop rows with NaN product names
    amazon_df['product_name'].replace('', np.NaN, inplace=True)
    amazon_df = amazon_df.dropna(subset=['product_name'])

    # Save the DataFrame to a CSV file
    amazon_df.to_csv('amazon_data.csv', header=True, index=False)
