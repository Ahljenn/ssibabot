import requests
from bs4 import BeautifulSoup

def xur_link():
	return 'https://wherethefuckisxur.com/'
  
URL = xur_link()
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
vendor = soup.find_all("div", class_="vendor-item")
xur_data = []

def find_xur():
  location = URL
  for i, link in enumerate(soup.find_all('img')):
    if i == 1:
      location += link.get('src')
      xur_data.append(location)

def find_items():
  for i, item in enumerate(vendor):
    ss = str(i+1) + '. ' + item.text.strip()
    xur_data.append(ss)