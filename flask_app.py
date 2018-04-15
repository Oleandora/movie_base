from flask import Flask, render_template, request
from movie_info import get_movie_data, save_movie_info, saved_movies, add_comment
from database import Movie

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results/', methods=['POST'])
def results():
    movie_to_search = request.form.get('movie_to_search')
    movie_data = get_movie_data(movie_to_search)
    return render_template('results.html', movie_data=movie_data )


@app.route('/save_to_db', methods=['POST'])
def save_to_db():
    movie_to_save = request.form.get('data')
    save_movie_info(movie_to_save)
    return render_template('save_to_db.html')


@app.route('/saved_movies')
def show_all():
    movies = saved_movies()
    return render_template('saved_movies.html', movies=movies)


@app.route('/comment_added', methods=['POST'])
def add():
    comment_to_add = request.form['comment']
    title = request.form['movie']
    add_comment(title, comment_to_add)
    movies = saved_movies()
    return render_template('saved_movies.html', movies=movies)


if __name__ == '__main__':
    app.run(port=8081, debug=True)