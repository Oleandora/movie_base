import requests
from bs4 import BeautifulSoup


def get_html(url, title=''):
    response = requests.get(url, params={'q': title, 'as_sitesearch': 'imdb.com'})
    return BeautifulSoup(response.content, 'html.parser')


def extract_title(html):
    raw_title = html.find(attrs={'class': 'originalTitle'}).text
    return raw_title.replace('(original title)', '').strip()


def extract_poster(html):
    return html.find(attrs={'class': 'poster'}).find('img')['src']


def extract_text_with_itemprop(html, itemprop):
    raw_data = html.findAll(itemprop=itemprop)
    return [data.text.strip().replace(',', '') for data in raw_data]


def extract_actors(html):
    return extract_text_with_itemprop(html, 'actors')


def extract_directors(html):
    return extract_text_with_itemprop(html, 'director')


def extract_genres(html):
    return extract_text_with_itemprop(html, 'genre')[:-1] # last element dublicate data in inappropriate way, so I cut off it


def extract_rating(html):
    return html.find(itemprop='ratingValue').text