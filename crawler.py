import re
# import sqlalchemy
import requests
from bs4 import BeautifulSoup as BS


STARTING_URL = 'http://register.start.bg/'
HISTOGRAM = {}
SITES_URLS = []


def get_response(*, url):
    try:
        response = requests.get(url, timeout=1)
        return response
    except Exception:
        print(f'Something went wrong while trying to access {url}')
        print(response)


def get_links_from_site(*, url):  # Finds all urls in html href tag
    found_urls = []

    response = get_response(url=url)

    if response:
        add_server_to_histogram(response=response)

        html = response.content.decode('utf-8')
        soup = BS(html, features='html.parser')

        for a in soup.find_all(href=True):
            url = re.match(r'https?://(.*)\.bg/?(.*)', str(a['href']))

            if url:
                found_urls.append(url.group())

    return found_urls


def add_server_to_histogram(*, response):
    key = response.headers["Server"]

    if key in HISTOGRAM.keys():
        HISTOGRAM[key] += 1
    else:
        HISTOGRAM[key] = 1


def add_urls_to_url_list(*, found_urls):
    for url in found_urls:
        if url not in SITES_URLS:
            SITES_URLS.append(url)


def bfs(url_list, index):
    if len(url_list) - 1 == index:
        return


def main():
    SITES_URLS.append(STARTING_URL)
    initialize_set = get_links_from_site(url=STARTING_URL)
    SITES_URLS.extend(initialize_set)

    print('SITES_SET\n', SITES_URLS)
    print('HISTOGRAM\n', HISTOGRAM)


if __name__ == '__main__':
    main()
