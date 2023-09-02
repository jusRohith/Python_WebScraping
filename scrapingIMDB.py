import requests, openpyxl
from bs4 import BeautifulSoup

# Define the URL and headers for the IMDb top-rated movies page
URL = 'https://www.imdb.com/chart/top/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                         'Version/16.6 Safari/605.1.15'}

# Create a new Excel workbook and sheet for storing movie data
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Top Rated Movies'

# Print the names of sheets in the workbook (useful for checking)
print(excel.sheetnames)

# Add headers to the Excel sheet
sheet.append(['Movie Rank', 'Movie Name', 'Year of Release', 'IMDB Rating'])

try:
    # Send an HTTP GET request to the IMDb page
    source = requests.get(URL, headers=HEADERS)
    source.raise_for_status()  # Raise an exception if the request was not successful
    soup = BeautifulSoup(source.content, 'html.parser')  # Parse the HTML content with BeautifulSoup

    # Find all elements containing movie data
    movies_data_list = soup.find_all('div', attrs={'class': 'ipc-metadata-list-summary-item__c'})

    # Iterate through each movie's data
    for movie in movies_data_list:
        # Extract relevant information
        rank = movie.find('h3', attrs={'class': 'ipc-title__text'}).text.split('. ')[0]
        movie_name = movie.find('h3', attrs={'class': 'ipc-title__text'}).text.split('. ')[1]
        year = movie.find('span', attrs={'class': 'sc-b85248f1-6 bnDqKN cli-title-metadata-item'}).text
        rating = (movie.find('span', attrs={
            'class': 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating'})
                  .text).split()[0]

        # Print and add the extracted data to the Excel sheet
        print(rank, movie_name, year, rating)
        sheet.append([rank, movie_name, year, rating])

except Exception as e:
    print(e)  # Print any exception that occurred during the execution

# Save the Excel workbook to a file
excel.save('./output/IMDB Movie Ratings.xlsx')
