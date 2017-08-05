from bs4 import BeautifulSoup
from urllib import urlopen
soup=BeautifulSoup(urlopen('http://google.com').read())
print soup.head.title