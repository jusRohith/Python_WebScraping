import requests
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':
    # Initialize variables
    URL = None
    webpage = None
    pages_data = []
    product_details = {'product_name': [], 'product_price': [], 'product_rating': []}

    # Loop to scrape data from multiple pages
    for i in range(1, 26):
        try:
            # Construct the URL for Flipkart search results
            URL = ('https://www.flipkart.com/search?q=gaming+console&sid=4rr%2Cx1m&as=on&as-show=on&otracker'
                   '=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_ps&as'
                   '-pos=1&as-type=RECENT&suggestionId=gaming+console%7CGaming+Consoles&requestId=f965eee8-135c-4da5-bf71'
                   f'-2535bc574bc9&as-searchtext=gaming&page={i}')
            # Make an HTTP GET request to the URL
            webpage = requests.get(URL)
            webpage.raise_for_status()  # Raise an exception if the request was not successful

            # Parse the HTML content and find all product links
            pages_data.append(BeautifulSoup(webpage.content, 'html.parser')
                              .find_all('a', attrs={'class': '_2rpwqI'}))
        except Exception as e:
            print(e)


    # Functions to extract product details from a product page

    def get_product_name(soup):
        try:
            product_name = (soup
                            .find('span', {'class': 'B_NuCI'})
                            .text
                            .strip())
        except AttributeError:
            product_name = ''
        return product_name


    def get_product_price(soup):
        try:
            product_price = (soup
                             .find('div', attrs={'class': '_30jeq3 _16Jk6d'})
                             .text
                             .strip())
        except AttributeError:
            product_price = ''
        return product_price


    def get_product_rating(soup):
        try:
            product_rating = (soup
                              .find('div', attrs={'class': '_3LWZlK'})
                              .text)
        except AttributeError:
            product_rating = ''
        return product_rating


    # Loop through the product links and scrape product details
    i = 1
    for page in pages_data:
        for product in page:
            # Construct the URL for the product
            new_url = 'https://www.flipkart.com' + product.get('href')
            new_webpage = requests.get(new_url)
            new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

            # Extract product details and add them to the dictionary
            product_details['product_name'].append(get_product_name(new_soup))
            product_details['product_price'].append(get_product_price(new_soup))
            product_details['product_rating'].append(get_product_rating(new_soup))
            print(i)  # Print to keep track of the number of products processed
            i = i + 1

    # Create a Pandas DataFrame from the collected product details
    flipkart_df = pd.DataFrame.from_dict(product_details)

    # Save the DataFrame to a CSV file
    flipkart_df.to_csv('flipkart_GamingConsoles_data.csv', header=True, index=False)
