import pandas as pd
import requests
from bs4 import BeautifulSoup, ResultSet


# Define functions to extract book information

def get_title(element):
    # Function to get the title of a book from an article element.
    try:
        image = element.find('img')
        title = image.attrs['alt']
    except AttributeError:
        title = ''
    return title


def get_price(element):
    # Function to get the price of a book from an article element.
    try:
        price = float(element.find('p', attrs={'class': 'price_color'}).text[1:])
    except AttributeError:
        price = 0.0
    return price


def check_availability(element):
    # Function to check the availability of a book from an article element.
    try:
        availability = element.find('p', attrs={'class': 'instock availability'}).text.strip()
    except AttributeError:
        availability = ''
    return availability


def get_rating(element):
    # Function to get the rating of a book from an article element.
    try:
        star = element.find('p')
        rating = star['class'][1]  # returns list
    except AttributeError:
        rating = ''
    return rating


# Create an empty list to store book details
books_details = []

# Iterate through pages to scrape book information
for i in range(1, 51):
    URL = f'https://books.toscrape.com/catalogue/page-{i}.html'
    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    articles: ResultSet = soup.find_all('article', attrs={'class': 'product_pod'})

    # Iterate through articles to extract book details
    for article in articles:
        # Extract book details and append to the list
        books_details.append([get_title(article), get_price(article), check_availability(article), get_rating(article)])

# Create a pandas DataFrame from the collected book details
df = pd.DataFrame(books_details, columns=['book_title', 'price_in_pounds', 'stock_availability', 'rating'])

# Save the DataFrame to a CSV file
df.to_csv('./output/books_data.csv')
