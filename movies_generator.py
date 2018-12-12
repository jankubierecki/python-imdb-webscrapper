from imdb import process_movie_url
from bs4 import BeautifulSoup
import json
import requests


def generate_data_for_genre(genre):
    items = get_movies(genre)
    with open('movies.json', 'w+') as f:
        json.dump(list(items), f)


def get_movies(genre):
    BASE_URL = 'https://www.imdb.com'
    search_pattern = '{}/search/title?genres={}'
    search_url = search_pattern.format(BASE_URL, genre)
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.select('h3.lister-item-header a')
    uris = [link['href'] for link in links]
    movie_urls = ['{}{}'.format(BASE_URL, uri) for uri in uris]
    items = (process_movie_url(url) for url in movie_urls)
    return items
