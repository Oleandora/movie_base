import requests, pprint
from bs4 import BeautifulSoup


def collect_data(html, imdb_id='0'):
    data = {}
    data['imdb ID'] = imdb_id
    data['poster'] = html.find(attrs={'class': 'poster'}).find('img')['src']
    data['title'] = html.find(attrs={'class': 'originalTitle'}).text.replace('(original title)','').strip()
    data['rating'] = html.find(itemprop='ratingValue').text

    tags = html.findAll("span", {"itemprop": "genre"})
    genres = []
    for genre in tags:
        genres.append(genre.text.strip())
    data['genre'] = genres

    tags = html.findAll(itemprop="actors")
    actors = []
    for actor in tags:
        actors.append(actor.text.strip().replace(',', ''))
    data['cast'] = actors

    tags = html.findAll(itemprop="creator")
    creators = []
    for creator in tags:
        creators.append(creator.text.strip().replace(',', ''))
    data['writers'] = creators

    directors = []
    tags = html.findAll(itemprop="director")
    for director in tags:
        directors.append(director.text.strip().replace(',', ''))
    data['directors'] = directors

    return data


def get_html(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


def get_url(title):
    try:
        if title[0:1] == 'tt':
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
