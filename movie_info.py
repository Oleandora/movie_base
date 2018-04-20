from parsing import *
from database import Movie, session


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


def str_to_list(data: str()):
    data = list(data.split(', '))
    return data


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


def search_movie_data(title):
    movies = session.query(Movie).filter(Movie.title.ilike('%{title}%'.format(title=title))).one()
    return movies


def add_comment_to_movie(movie, comment):
    movie.comments = comment


def add_comment(title, comment):
    movie = search_movie_data(title)
    add_comment_to_movie(movie, comment)
    session.commit()



