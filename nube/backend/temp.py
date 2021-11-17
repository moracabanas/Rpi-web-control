from bs4 import BeautifulSoup
import requests

url = 'https://sostaskillbox.it'

r = requests.get(url+'/news')

soup = BeautifulSoup(r.content, 'html.parser')

urls = []
for img in soup.find_all('img', {'class':'elementor-animation-grow attachment-large size-large'}):
    link= img.find_parent('a')['href']
    if(link[0]=='/'):
        link=url+link
    elif(link[0]=='#'):
        link=url
    urls.append(link)
    