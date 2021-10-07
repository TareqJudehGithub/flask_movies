from flask import Flask, render_template, url_for
from markupsafe import escape
import requests

app = Flask(__name__)

omdb_api = "http://www.omdbapi.com/?apikey=deec4c57&s=batman"
data = requests.get(url=omdb_api)


# mainpage route
@app.route("/")
def mainpage():

  movies = data.json()

  return render_template(
    escape("index.html"),
    movies=movies
  )


# search movies route
@app.route("/<title>")
def movies_by_title(title):
  movies = requests.get(
    url="http://www.omdbapi.com/?apikey=deec4c57&s=" + title
  ).json()

  return render_template(
    escape("index.html"),
    movies=movies
  )


# movie information route
@app.route("/movie_info/<title>")
def movie_info(title):
  movie = requests.get(
    url="http://www.omdbapi.com/?apikey=deec4c57&t=" + title
  ).json()

  return render_template(
    escape("movie-info.html"),
    movie=movie
  )

  
if __name__ == '__main__':
  app.run(debug=True)

