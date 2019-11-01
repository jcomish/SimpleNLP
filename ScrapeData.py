import requests
from bs4 import BeautifulSoup as bs
import os

_URL = 'http://proceedings.mlr.press/v80/'

r = requests.get(_URL)
soup = bs(r.text)

r = requests.get(_URL)
soup = bs(r.text)
urls = []
names = []
for i, link in enumerate(soup.findAll('a')):
    if "Download PDF" in link.contents or "Supplementary PDF" in link.contents:
        _FULLURL = link.get('href')
        if _FULLURL.endswith('.pdf'):
            urls.append(_FULLURL)
            names.append(soup.select('a')[i].attrs['href'])

names_urls = zip(names, urls)
os.chdir('PDFs')

for name, url in names_urls:
    print('Downloading %s' % url)
    os.system('wget %s' % url)