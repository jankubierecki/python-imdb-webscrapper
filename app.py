from flask import Flask, render_template, redirect, url_for, request
import json

from movies_generator import generate_data_for_genre

app = Flask(__name__)


@app.route("/")
def index():
    categories = [
        'fantasy',
        'comedy',
        'western'
    ]
    with open('movies.json', 'r', encoding='utf-8') as f:
        movies = json.load(f)

    return render_template("movies.html", movies=movies, categories=categories)


@app.route("/change-category", methods=['POST'])
def change_category():
    genre = request.form['movie_category']
    generate_data_for_genre(genre)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
