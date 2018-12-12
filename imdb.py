import requests
import json

from bs4 import BeautifulSoup
from functools import reduce


def extract_movie(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    meta_raw = soup.select_one(
        'script[type="application/ld+json"]')
    metadata = json.loads(meta_raw.text)
    return metadata


mappings = {
    "title": 'name',
    "description": 'description',
    "director": 'director',
    "actors": 'actor',
    "rating": 'aggregateRating',
    "cover_url": 'image',
    'pg': 'contentRating',
    'published': 'datePublished'
}


def map_to_movie_row(data):
    return {
        own_key: data.get(external_key, None) for own_key, external_key in mappings.items()
    }


def clean_actors(raw_actors):
    return ", ".join(actor['name'] for actor in raw_actors)


def clean_directors(one_or_many):
    if isinstance(one_or_many, list):
        return clean_actors(one_or_many)

    if one_or_many:
        return one_or_many['name']

    return "gall ANonim"


cleaners = {
    "actors": clean_actors,
    "rating": lambda x: x['ratingValue'] if x else 0,
    "director": clean_directors,
    'pg': lambda x: x.replace("PG-", "") if x else 18
}


def apply_cleaners(row):
    for key, cleaner in cleaners.items():
        row[key] = cleaner(row[key])
    return row


def process_movie_url(url):
    pipe = [
        extract_movie,
        map_to_movie_row,
        apply_cleaners
    ]
    return reduce(lambda result, fn: fn(result), pipe, url)
