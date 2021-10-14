from flask import Flask, render_template, url_for, request, flash, session,\
  redirect
from markupsafe import escape
import requests
import os, pprint

# Flask secret key
secret_key = os.urandom(12)


app = Flask(__name__)

# app.config["SECRET KEY"] = secret_key

app.secret_key =  secret_key


# omdb API 
omdb_key = os.environ.get("OMDB_KEY")
response = f"http://www.omdbapi.com/?apikey={omdb_key}&s=home&type=movie"
data = requests.get(url=response)


@app.route('/')     # homepage route
def homepage():

  movies = data.json()

  return render_template(
      escape("index.html"),
      movies=movies
)

# movie details page
@app.route("/movie-info/<title>")
def movie_info(title):
    movie = requests.get(
        url=f"http://www.omdbapi.com/?apikey={omdb_key}&t={title}"
    ).json()
     
    return render_template(
        escape("movie-info.html"),
        movie=movie
    )


# selected movie titles
@app.route("/<title>")
def movies_by_title(title):
  movies = requests.get(
      url=f"http://www.omdbapi.com/?apikey={omdb_key}&s={title}"
  ).json()

  return render_template(
      escape("index.html"),
      movies=movies
  )


# search form
@app.route('/search-movies', methods=["GET", "POST"])
def search_movies():
  if request.method == "POST":
    title = request.form["title"]
    year = request.form["year"]
    type = request.form["type"]
        
    # advanced search filters
    if year != "" or type != "":
        movie = requests.get(
          url=f"http://www.omdbapi.com/?apikey=deec4c57&t={title}&y={year}&type={type}"
          ).json()
    else:
      movie = requests.get(
        url=f"http://www.omdbapi.com/?apikey={omdb_key}&t={title}"
      ).json()

    # title not found flash message
    if movie["Response"] == "False":
      flash("Title not found!")
      return render_template(
        escape("search-form.html")
      )
      
    return render_template(
        escape("search-form.html"),
        movie=movie
    )
  else:
    return render_template(
          escape("search-form.html")
    )


# search form - link
@app.route('/search-nav', methods=["POST"])
def search_nav():

    search_mov = request.form["search_mov"]
    
    movies = requests.get(url=f"http://www.omdbapi.com/?apikey={omdb_key}&s={search_mov}").json()

    # title not found flash message
    if movies["Response"] == "False":
      flash("Title not found! Kindly check title spelling and try again.")
      return render_template(
        escape("search-form.html")
      )
    
    return render_template(
        escape("search-nav.html"),
        movies=movies
     )
  

# ===========================================================
  # # in case movie title was not found
  # flash("Movie not found!")

  # if movie["Response"] == "False":
  #   return "Movie not found :("

  # return render_template(escape("search-form.html"), movie=movie)

  
# Favorites
@app.route("/fav_movies")
def fav_movies():
  
  # get session:
  fav_list = session.get("favorites")
  print(f"fav_list: {fav_list}")


  if  fav_list == None:
    flash("Your Favorites list is empty")
    
    print(f"fav_list is None: {fav_list}")
    return redirect(url_for("homepage"))

  else:
    print(f"fav_list is occupied now: {fav_list}")
    return render_template(
      escape("fav-movies.html"),
      fav_list=fav_list
    )


# add movies to favorites
@app.route("/add_to_fav/<title>")
def add_to_fav(title):
  """add movies to Favorites function"""

  fav_dict = dict()
  # check if favorites exists
  if "favorites" in session:
    # add fav key to fav_dict
   fav_dict = session.get("favorites")
  
  else:
    # create a new fav key
    session["favorites"] = dict()
  
  print(f"fav_dict before: {fav_dict}")

  # store movie in favorites dict
  fav_dict[title] = title

  print(f"fav_dict after: {fav_dict}")

  # add key to session
  session["favorites"] = fav_dict

  return redirect(url_for('homepage'))


# remove movies from favorites
@app.route("/remove_mov<title>")
def remove_movie(title):

  # call favorites
  fav_dict = session.get("favorites")
  print(f"Favorites (remove route before removal): {fav_dict}")
  # remove movie from favorites
  fav_dict.pop(title, None)

  # update session
  session["favorites"] = fav_dict
  print(f"Favorites (remove route after removal): {fav_dict}")

  return redirect(url_for("fav_movies"))






if __name__ == '__main__':
  app.run(debug=True)

