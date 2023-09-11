import requests
from bs4 import BeautifulSoup
url = 'https://medium.com/@Evenword/python-for-ethical-hacking-techniques-and-tools-15aaf04b4214'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
data = soup.find_all()
for item in data:
    print(item.text)