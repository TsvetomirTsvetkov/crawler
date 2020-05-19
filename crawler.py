import re
import requests
from bs4 import BeautifulSoup as BS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column
from contextlib import contextmanager
from settings import DB_NAME

STARTING_URL = 'http://register.start.bg/'
OUR_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
}
HISTOGRAM = {}
SITES_URLS = []


engine = create_engine(f"sqlite:///{DB_NAME}")
Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Server(Base):
    __tablename__ = 'Server'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(Integer)


def get_response(*, url):
    try:
        response = requests.get(url, timeout=3, headers=OUR_HEADERS)
        return response
    except Exception:
        print(f'[Something went wrong while trying to get response from {url}]')


def get_links_from_site(*, url):
    found_urls = []

    response = get_response(url=url)

    if response and response.status_code == 200:
        add_server_to_histogram(response=response)
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


def bfs(*, url_list, index):
    if len(url_list) - 1 == index:
        return

    found_urls = get_links_from_site(url=url_list[index])

    add_urls_to_url_list(found_urls=found_urls)

    fill_db(servers=HISTOGRAM)

    bfs(url_list=url_list, index=index + 1)


def fill_db(*, servers):
    with session_scope() as session:
        for key in servers.keys():
            server = session.query(Server).filter(Server.name == key).first()

            if server:
                server.number = servers[key]
            else:
                session.add(Server(name=key, number=servers[key]))


def main():
    Base.metadata.create_all(engine)

    SITES_URLS.append(STARTING_URL)
    initialize_set = get_links_from_site(url=STARTING_URL)
    SITES_URLS.extend(initialize_set)

    bfs(url_list=SITES_URLS, index=0)

    print(HISTOGRAM)


if __name__ == '__main__':
    main()
