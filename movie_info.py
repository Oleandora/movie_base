import requests, ast
from bs4 import BeautifulSoup
from database import Movie, session


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


def collect_data(html, imdb_id='0'):
    return {
        'imdbid': imdb_id,
        'poster': extract_poster(html),
        'title': extract_title(html),
        'rating': extract_rating(html),
        'genre': extract_genres(html),
        'cast': extract_actors(html),
        'directors': extract_directors(html),
        'comments': '',
    }


def get_html(url, title=''):
    response = requests.get(url, params={'q': title, 'as_sitesearch': 'imdb.com'})
    return BeautifulSoup(response.content, 'html.parser')


def find_imdb_content(html):
    cite = html.find('cite')
    if 'imdb.com/title/tt' in cite.text:
        html = get_html('http://{0}'.format(cite.text))
        get_imdb_id = cite.text.replace('/', '').split('title')
        imdb_id = get_imdb_id[1]
        return html, imdb_id
    else:
        return 'Can\'t find movie title in Google :(', 'Sorry about that.'


def get_movie_data(title):
    try:
        html = get_html('https://www.google.com/search', title)
        html, imdb_id = find_imdb_content(html)
        movie = collect_data(html, imdb_id)
        return prepare_record(movie)
    except Exception as e:
        return 'Error: ', e.args[0]


def list_to_str(data: list):
    if isinstance(data, str):
        return data
    else:
        data = ', '.join(data)
        return data


def prepare_record(data):
    data['rating'] = float(data['rating'])
    data['cast'] = list_to_str(data['cast'])
    data['directors'] = list_to_str(data['directors'])
    data['genre'] = list_to_str(data['genre'])
    record = Movie(**data)
    return record


def save_movie_info(movie):
    movie = prepare_record(ast.literal_eval(movie))
    session.add(movie)
    session.commit()


def saved_movies():
    return session.query(Movie).all()


def str_to_list(data: str()):
    data = list(data.split(', '))
    return data


def search_movie_data(title):
    movies = session.query(Movie).filter(Movie.title.ilike('%{title}%'.format(title=title))).one()
    return movies


def choose_movie(movie_list):
    for number, movie in enumerate(movie_list):
        print(number, movie.title)
    selected_movie = int(input('Enter movie number to comment'))
    return movie_list[selected_movie]


def add_comment_to_movie(movie, comment):
    movie.comments = comment


def add_comment(title, comment):
    movie = search_movie_data(title)
    add_comment_to_movie(movie, comment)
    session.commit()



