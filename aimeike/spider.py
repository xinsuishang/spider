import requests
from bs4 import BeautifulSoup

url = 'https://aimeike.tv/category'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
source_list = soup.find('div', class_="category-gallery").find_all('a', class_="category-item theme-item card js-category-item")
target = []
for source in source_list:
    data = {
        'title': source.find('h5').get_text(),
        'tag': source.find('time').get_text(),
        'user_counet': source.find('span').get_text(),
        'text': source.find('p').get_text(),
    }
    target.append(data)
