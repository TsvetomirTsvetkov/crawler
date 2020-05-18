import re
# import sqlalchemy
import requests
from bs4 import BeautifulSoup as BS


STARTING_URL = 'http://register.start.bg/'

response = requests.get(STARTING_URL).content

html = response.decode('utf-8')

starting_soup = BS(html, features="html.parser")


found_urls = []


def main():
    for a in starting_soup.find_all(href=True):
        url = re.match('https?://(.*).bg/?', str(a['href']))

        if url:
            print("Found URL:", url.group())


if __name__ == '__main__':
    main()
