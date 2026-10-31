#main.py

from fastapi import FastAPI, Query
from fastapi import File, UploadFile, HTTPException
from src import MovieInput, MovieResponse, DataStorage, CSVInfo, ProcessConfig
from pathlib import Path
import logging
import io
import pandas as pd
from middleware import log_requests

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

app.middleware("http")(log_requests)

storage = DataStorage()

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


@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read() # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename,"size_bytes": len(contents)}


@app.get("/demo/movie-lookup/{movie_id}", response_model=MovieResponse)
def demo_lookup_movie(movie_id: int):
    movie = movies.get(movie_id)

    if movie is None:
        logger.warning(f"Movie not found: {movie_id}")
        raise HTTPException( status_code=404, detail="Movie not found")

    return movie


@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    # TODO 2: check the filename extension using pathlib.
        # Reject non-CSV files with status 400 and log a WARNING.
    if not file.filename:
        logger.warning(f"{file} has no attribute .filename")
        raise HTTPException(status_code=400, detail="No filename")
    path = Path(file.filename)
    if path.suffix != ".csv":
        logger.warning(f"{path} has wrong file type, need.csv.")
        raise HTTPException(status_code=400, detail="Wrong file type")
    

    # TODO 3: await the file contents and parse the CSV.
    # Catch expected parsing/decoding errors (e.g. EmptyDataError,ParserError, UnicodeDecodeError) and raise HTTPException
    # with status_code=400.
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except(pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as error:
        logger.warning(f"Cannot read CSV: {error}")
        raise HTTPException(status_code=400, detail="Cannot read the uploaded CSV")

    
    # TODO 4: save the DataFrame with storage.save_data().
    # Log the dataset ID, filename at INFO.
    # Return a CSVInfo object with the ID, filename, shape, and column names.
    storage.save_data(df, file.filename)
    logger.info(f"File saved with ID: {storage.counter}, filename: {file.filename}")
    return CSVInfo(filename=file.filename, rows = len(df), 
                   columns = len(df.columns), column_names= df.columns.tolist(), 
                   dataset_id=storage.counter)


@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    # TODO 5: get the DataFrame using storage.get_data().
    # If it is missing, log a WARNING and raise HTTPException with status 404.
    # Otherwise, log successful retrieval at INFO.
    # Return a dictionary with dataset_id, rows, and columns.
    data = storage.get_data(dataset_id)
    if data is None:
        logger.warning(f"Dataset not found at id {dataset_id}")
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    logger.info(f"Successful retrieval of dataset with id {dataset_id}")
    shape_dict = {"dataset_id": dataset_id, "rows": len(data), 
                  "columns": len(data.columns)}
    return shape_dict


@app.post("/demo/process-config")
def demo_process_config(config: ProcessConfig):
    df = pd.DataFrame({"title": ["Movie A", "Movie A", "Movie B", None]})
    settings = config.model_dump()
    if settings["processing"]["remove_duplicates"]:
        df = df.drop_duplicates()
    if settings["processing"]["drop_missing"]:
        df = df.dropna()

    return {"rows": len(df)}
    