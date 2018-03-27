import requests, pprint
from bs4 import BeautifulSoup


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


def extract_creators(html):
    return extract_text_with_itemprop(html, 'creator')


def extract_directors(html):
    return extract_text_with_itemprop(html, 'director')


def extract_genres(html):
    return extract_text_with_itemprop(html, 'genre')


def extract_rating(html):
    return html.find(itemprop='ratingValue').text


def collect_data(html, imdb_id='0'):
    return {
        'imdb ID': imdb_id,
        'poster': extract_poster(html),
        'title': extract_title(html),
        'rating': extract_rating(html),
        'genre': extract_genres(html),
        'cast': extract_actors(html),
        'creators': extract_creators(html),
        'directors': extract_directors(html),
    }


def get_html(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


def get_url(title):
    try:
        if title.startswith('tt'):
            html = get_html('http://www.imdb.com/title/{title}/'.format(title=title))
            imdb_id = title

        else:
            html = get_html('https://www.google.com/search?q={title}'.format(title=title))
            for cite in html.findAll('cite'):
                if 'imdb.com/title/tt' in cite.text:
                    html = get_html('http://{0}'.format(cite.text))
                    get_imdb_id = cite.text.replace('/', '').split('title')
                    imdb_id = get_imdb_id[1]
                    break
            else:
                return 'Can\'t find movie title in Google :( Sorry about that.'
        return collect_data(html, imdb_id)
    except Exception as e:
        return 'Error: ', e.args[0]


if __name__ == '__main__':
    movie_name = input("Enter imdb ID or title of the movie: ")
    pprint.pprint(get_url(movie_name))
