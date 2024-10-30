from fastapi import FastAPI, Path, HTTPException, Query
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Movie:
    id: int
    title: str
    gender: str
    age: int
    
    def __init__(self, id, title, gender, age, ):
        self.id = id
        self.title = title
        self.gender = gender
        self.age = age

class MovieResquest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    gender: str = Field(min_length=3)
    age: int = Field(gt=0, lt=19)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new Movie",
                "gender": "action",
                "age": 12,
            }
        }
    }
        

MOVIES = [
        Movie(1, 'Avengers','action', 12),
        Movie(2, 'Spider-Man','action', 12 ),
        Movie(3, 'Alone','horror', 18 ),
        Movie(4, 'Nemo','adventure', 10 ),
        Movie(5, 'Frozen','animation', 10 )
]
        
#Pega todos os filmes
@app.get('/movies', status_code= status.HTTP_200_OK)
async def read_all_movies():
   return MOVIES

#Pega todos com o titulo especifico
@app.get('/movies/{title}', status_code= status.HTTP_200_OK)
async def read_movies_by_title(title:str):
    movies_by_title = [movie for movie in MOVIES if movie.title.lower() == title.lower()]
    if movies_by_title:
        return movies_by_title
    raise HTTPException(status_code = 404, detail='Item not found')

#Pega todos com id especifico
@app.get('/movies/{movie_id}', status_code= status.HTTP_200_OK)
async def read_movie(movie_id: int):
    for movie in MOVIES:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code = 404, detail='Item not found')
    
#Pega todos de um genero especifico     
@app.get('/movies/gender/{gender}', status_code= status.HTTP_200_OK)
async def read_movies_by_gender(gender:str):
    movies_by_gender = [movie for movie in MOVIES if movie.gender.lower() == gender.lower()]
    if movies_by_gender:
        return movies_by_gender
    raise HTTPException(status_code = 404, detail='Item not found')
    
#Metodo de add filme
@app.post ('/create-movie', status_code=status.HTTP_201_CREATED)
async def create_movie(movie_request: MovieResquest):
    new_movie = Movie(**movie_request.model_dump())
    MOVIES.append(find_movie_id(new_movie))

#def de criar ID a partir do ultimo para o metodo de add
def find_movie_id(movie: Movie):
    movie.id = 1 if len(MOVIES) == 0 else MOVIES[-1].id + 1
    return movie

@app.put ('/movies/update_movie', status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(movie: MovieResquest):
    movie_changed = False
    for i in range(len(MOVIES)):
        if MOVIES[i].id == movie.id:
            MOVIES[i] = movie
            movie_changed = True
    if not movie_changed:
        raise HTTPException(status_code = 404, detail='Item not found')
    
@app.delete ('/movies/{movies_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int):
    movie_changed = False
    for i in range(len(MOVIES)):
        if MOVIES[i].id == movie_id:
            MOVIES.pop(i)
            movie_changed = True
            break
    if not movie_changed:
        raise HTTPException(status_code = 404, detail='Item not found')