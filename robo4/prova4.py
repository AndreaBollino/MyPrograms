import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
url = 'https://www.example.com'

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links on the page
links = soup.find_all('a')

# Print the links
for link in links:
    print(link.get('href'))