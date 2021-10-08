from flask import Flask, render_template, url_for, request, flash, session,\
  redirect
from markupsafe import escape
import requests
import os


app = Flask(__name__)

omdb_key = os.environ.get("OMDB_KEY")
app.config["SECRET_KEY"] = omdb_key

# Flask secret key
secret_key = os.urandom(12)
app.secret_key =  secret_key


omdb_api = f"http://www.omdbapi.com/?apikey={omdb_key}&s=batman"
data = requests.get(url=omdb_api)

# mainpage route
@app.route("/")
def mainpage():

  movies = data.json()

  return render_template(
    escape("index.html"),
    movies=movies
  )

# change webpage dynamically
@app.route("/string:<webpage>")
def render_page(webpage):
  return render_template(webpage)


# search movies route
@app.route("/<title>")
def movies_by_title(title):
  movies = requests.get(
    url=f"http://www.omdbapi.com/?apikey=deec4c57&s={title}"
  ).json()

  return render_template(
    escape("index.html"),
    movies=movies
  )


# movie information route
@app.route("/movie_info/<title>")
def movie_info(title):
  movie = requests.get(
    url=f"http://www.omdbapi.com/?apikey=deec4c57&t={title}"
  ).json()

  return render_template(
    escape("movie-info.html"),
    movie=movie
  )

# search form
@app.route("/search-form")
def search_form():
  return render_template(escape("search-form.html"))


# search by title
@app.route("/search_title", methods=["POST"])
def search_title():
  # data = request.form.to_dict()
  # title = data["title"]
  # year = data["year"]
  title = request.form["title"]
  year = request.form["year"]
 
  # in case user filled in Year field
  if  year != "":
    movie = requests.get(
      url=f"http://www.omdbapi.com/?apikey=deec4c57&t={title}&y={year}"
    ).json()
  else:
    movie = requests.get(
      url=f"http://www.omdbapi.com/?apikey=deec4c57&t={title}"
    ).json()
  

  # in case movie title was not found
  flash("Movie not found!")

  if movie["Response"] == "False":
    return "Movie not found :("

  return render_template(escape("search-form.html"), movie=movie)


# combine both search_form and search_title in one route
  
# Favorites
@app.route("/fav_movies")
def fav_movies():
  
  # get session:
  fav_list = session.get("favorites")
  if  fav_list is  None:
    return redirect(url_for("mainpage"))
  else:
    return render_template(
      escape("fav-movies.html"),
      fav_list=fav_list
    )


if __name__ == '__main__':
  app.run(debug=True)

