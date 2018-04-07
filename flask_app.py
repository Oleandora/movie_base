from flask import Flask, render_template, request
from movie_info import get_movie_data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results/', methods=['POST'])
def results():
    movie_to_search = request.form.get('movie_to_search')
    movie_data = get_movie_data(movie_to_search)
    return render_template('results.html', movie_data=movie_data )



if __name__ == '__main__':
    app.run(port=8081, debug=True)