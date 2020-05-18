import re
# import sqlalchemy
import requests
from bs4 import BeautifulSoup as BS


STARTING_URL = 'http://register.start.bg/'
HISTOGRAM = {}
SETS = set()


def get_links_from_site(*, url):  # Finds all urls in html href tag
    found_urls = set()

    try:
        response = requests.get(url, timeout=1).content
    except Exception:
        print(f'Something went wrong while trying to access {url}')
        print(response)
        return found_urls

    html = response.decode('utf-8')
    soup = BS(html, features='html.parser')

    for a in soup.find_all(href=True):
        url = re.match(r'https?://(.*)\.bg/?(.*)', str(a['href']))

        if url:
            found_urls.add(url.group())

    return found_urls


def bfs():
    pass


def main():
    print(len(get_links_from_site(url='http://register.start.bg/')))


if __name__ == '__main__':
    main()
