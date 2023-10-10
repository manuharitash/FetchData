import requests
from bs4 import BeautifulSoup

url = 'https://insights.blackcoffer.com/rise-of-telemedicine-and-its-impact-on-livelihood-by-2040-3-2/'

response = requests.get(url)

htmlContent = response.content
soup = BeautifulSoup(htmlContent, 'html.parser')

title = soup.title
print(title)

print(soup.find_all('div', class_="td-post-content"))
body = soup.find('p').get_text()
path = url + ".txt"
with open('readme.txt', 'p') as f:
    f.write(body)

