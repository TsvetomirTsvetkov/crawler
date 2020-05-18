import re
# import sqlalchemy
import requests
from bs4 import BeautifulSoup as BS


STARTING_URL = 'http://register.start.bg/'
HISTOGRAM = {}
SITES_SET = set()  # TODO: Change type to list


def get_response(*, url):
    try:
        response = requests.get(url, timeout=1)
        return response
    except Exception:
        print(f'Something went wrong while trying to access {url}')
        print(response)


def get_links_from_site(*, url):  # Finds all urls in html href tag
    found_urls = set()

    response = get_response(url=url)

    if response:
        add_server_to_histogram(response=response)

        html = response.content.decode('utf-8')
        soup = BS(html, features='html.parser')

        for a in soup.find_all(href=True):
            url = re.match(r'https?://(.*)\.bg/?(.*)', str(a['href']))

            if url:
                found_urls.add(url.group())

    return found_urls


def add_server_to_histogram(*, response):
    key = response.headers["Server"]

    if key in HISTOGRAM.keys():
        HISTOGRAM[key] += 1
    else:
        HISTOGRAM[key] = 1


def bfs():
    pass


def main():
    SITES_SET.add(STARTING_URL)
    initialize_set = get_links_from_site(url=STARTING_URL)
    SITES_SET.update(initialize_set)

    print('SITES_SET\n', SITES_SET)
    print('HISTOGRAM\n', HISTOGRAM)


if __name__ == '__main__':
    main()
