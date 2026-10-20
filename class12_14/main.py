#main.py

from fastapi import FastAPI, Query
from src import MovieInput, MovieResponse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}

app = FastAPI(title="Movie API")


@app.get("/health")
def health_check():
    return {"status": "ok"}

#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}

#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}

@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    # movie.title --> "Movie C"
    # movie.release_year --> 2022
    # both from MovieInput, required inputs for post
    return movie.model_dump() # Converts the model to a python dictionary.
    #output ex: {"title": "Movie C", "release_year": 2022}

demo_movie_examples: list = []

@app.post("demo/movie-examples",
          response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump() # turning input (movie) into a dict titled record
    record["id"] = movie_id # adding id to the record
    demo_movie_examples.append(record) # adding to the global variable
    return record # return the dictionary with the added id value

    """ Can also use this response model for a list of movies:

    response_model=list[MovieResponse]: expects a list of movies.
    ...
    return [record]"""



@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    # TODO 1: return up to limit movies as a list.
    # Log the number returned at INFO.
    # hint: movies is a dictionary whose values are movie records.
    movie_list: list = []
    for i, movie in enumerate(movies.values()):
        if i < limit:
            movie_list.append(movie)
    logger.info(f"{len(movie_list)} movies returned")
    return movie_list

@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    # TODO 2: 
    # Convert movie to a dictionary, add the new ID, and store it.
    # Log the new ID at INFO and return the stored record.
    record = movie.model_dump()
    id = len(movies) + 1
    record["id"] = id
    movies[id] = record
    logger.info(f"New movie added with ID {id}")
    return record
    