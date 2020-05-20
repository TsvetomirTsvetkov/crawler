import re
import requests
from bs4 import BeautifulSoup as BS
from .model import Model


class Controller:
    STARTING_URL = 'http://register.start.bg/'
    OUR_HEADERS = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }
    HISTOGRAM = {}
    SITES_URLS = []

    def __init__(self):
        self.model = Model

    def see_db(self):
        return self.model.see_db()

    def fill_db(self, servers):
        self.model.fill_db(servers)

    def start_crawling_without_stopping(self):
        Controller.SITES_URLS.append(Controller.STARTING_URL)
        initialize_set = self.get_links_from_site(url=Controller.STARTING_URL)
        Controller.SITES_URLS.extend(initialize_set)

        self.bfs(url_list=Controller.SITES_URLS, index=0)

    def get_links_from_site(self, url):
        found_urls = []

        response = self.get_response(url=url)

        if response and response.status_code == 200:
            self.add_server_to_histogram(response=response)
            print(url)
            try:
                html = response.content.decode('utf-8')
                soup = BS(html, features='html.parser')

                for a in soup.find_all(href=True):
                    url = re.match(r'https?://(.*)\.bg/?(.*)', str(a['href']))  # TODO: Remove unecessary parts of urls

                    if url:
                        found_urls.append(url.group())
            except Exception:
                print(f'[Something went wrong while crawling {url}]')

        return found_urls

    def bfs(self, url_list, index):  # Make it work without recursion?
        if len(url_list) - 1 == index:
            return

        found_urls = self.get_links_from_site(url=url_list[index])

        self.add_urls_to_url_list(found_urls=found_urls)

        self.fill_db(servers=Controller.HISTOGRAM)

        self.bfs(url_list=url_list, index=index + 1)

    def add_urls_to_url_list(self, found_urls):
        for url in found_urls:
            if url not in Controller.SITES_URLS:
                Controller.SITES_URLS.append(url)

    def add_server_to_histogram(self, response):
        try:
            key = response.headers["Server"]

            if key in Controller.HISTOGRAM.keys():
                Controller.HISTOGRAM[key] += 1
            else:
                Controller.HISTOGRAM[key] = 1
        except Exception:
            print("[Couldn't find server tag]")

    def get_response(self, url):
        try:
            response = requests.get(url, timeout=3, headers=Controller.OUR_HEADERS)
            return response
        except Exception:
            print(f'[Something went wrong while trying to get response from {url}]')

    def get_analytics(self, hour=False, day=False, month=False):
        return self.model.get_analytics(hour=hour, day=day, month=month)
