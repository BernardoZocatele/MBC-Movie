from database_connect import addUserDb, checkLogin, takeId, saveMovieDB, takeUsername, takeMyMovies, checkSaveMovie, takeVotes, mediaRate
from datetime import timedelta
from fastapi import FastAPI, Request, Query, Form, Request, HTTPException, Depends, Response 
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse, RedirectResponse
from function import buscar_filme, get_gender, create_id, popularFilms, similar_films
from get_images import get_poster
from hashe import hash_password
from schemas import filmModel, userModel
from auth_utils import create_jwt
from jwt import PyJWTError
import jwt

SECRET_KEY = "*UgtU@66TR--pDf44e"
ALGORITHM = "HS256"

app = FastAPI()

templates = Jinja2Templates(directory = "templates")

def get_current_user(request: Request):
    token = request.cookies.get("auth_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado. É necessário fazer login para acessar essa página")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    return user_id

# LOGIN AREA

@app.get('/')   
def login_cadastro(request: Request, response: Response):
    
    response = templates.TemplateResponse(
        request = request, name = "login.html"
    )
    response.delete_cookie("auth_token")
    
    return response

@app.get('/createUser/')
def create_user(newUser: str, newPassword: str):
    hashedPassword = hash_password(newPassword)
    user = userModel(user_id = create_id(), username = newUser, password = hashedPassword)
    addUserDb(user)
    
    return RedirectResponse(url="/")

@app.post("/loginUser")
def login_user(loginUser: str = Form(...), loginPassword: str = Form(...)):
    if checkLogin(loginUser, loginPassword) == 0:
        userId = takeId(loginUser)
        
        token = create_jwt(userId)
        response = RedirectResponse(url="/homePage", status_code=303)
        response.set_cookie(key="auth_token", value=token, httponly=True, samesite="Lax", expires=timedelta(minutes=30))
        
        return response
        
    else: return {'message': 'Falha no Login'}    
    
@app.get('/logout', response_class = RedirectResponse)
def logoutUser(response: Response):
    response = RedirectResponse(url = "/")
    response.delete_cookie("auth_token") 
    
    return response
    

# SEARCH AREA

    
@app.get('/search/{film_name}', response_class = HTMLResponse)
def read_root(request: Request, film_name: str, user_id: dict = Depends(get_current_user)):
    similarPosters = []
    
    title, sinopse, genders, release, poster_path =  buscar_filme(film_name)
    poster = get_poster(poster_path)
    username = takeUsername(user_id)
    
    genderList = get_gender(genders)
    delimiter = ", "
    gender_str = delimiter.join(genderList)
    
    similarFilms = similar_films(genders[0], title)
    
    media = mediaRate(title)
    
    for film in similarFilms:
        temp = get_poster(film['poster_path'])
        similarPosters.append(temp)
        
    return templates.TemplateResponse(
        request = request, name="item.html", context={"title": title, "sinopse": sinopse, "genders": gender_str, "release": release,"imagem": poster, "username": username, "similarPosters": similarPosters, "similarFilms": similarFilms, "mediaRate": media}
    )
    
@app.get('/homePage', response_class = HTMLResponse)
def get_templates(request: Request, user_id: dict = Depends(get_current_user)):
    
    username = takeUsername(user_id)
    
    posters = []
    films = popularFilms()
    for film in films:
        image = get_poster(film['poster_path'])

        posters.append(image)
    
    return templates.TemplateResponse(
        request = request, name="home.html", context={ "filmes": films, "posters": posters, "username": username}
    )
    
    
@app.get('/temp', response_class = RedirectResponse)
async def redirect_search( q: str = Query(...)):
    return RedirectResponse(url=f"/search/{q}")


# DATA BASE MOVIE AREA


@app.get('/saveMovie', response_class = RedirectResponse)
def addMovie(request: Request, title: str, genders: str, movieRelease: str, user_id: dict = Depends(get_current_user)):
    
    if checkSaveMovie(title, user_id) == 0:
        infosMovie = filmModel(user_id = user_id, movie = title, gender = genders, release = movieRelease)
        saveMovieDB(infosMovie)
        return RedirectResponse(url="/homePage")
    else:
        username = takeUsername(user_id)
        message = "Esse filme já foi adicionado na lista do usuário"
        return templates.TemplateResponse(
            request = request, name = 'error.html', context={"username": username, "message": message}
        )
        

@app.get('/myMovies', response_class = HTMLResponse)
def getMyMovies(request: Request, user_id: dict = Depends(get_current_user)):
    results, posters = takeMyMovies(user_id)
    username = takeUsername(user_id)
    
    return templates.TemplateResponse(
        request = request, name = "my_save.html", context={"results": results, "posters": posters, "username": username}
    )    
    
@app.get('/rateMovie', response_class = RedirectResponse)
def rateMovie(request: Request, star: int, movie: str, user_id: dict = Depends(get_current_user)):
    if takeVotes(movie, star) == 0:
        return RedirectResponse(url=f'/search/{movie}')
    else:
        username = takeUsername(user_id)
        message = "Não foi possível avaliar o filme, tente mais tarde!"
        
        return templates.TemplateResponse(
            request = request, name = "error.html", context={"username": username, "message": message}
        )
    
@app.get('/erro/', response_class = HTMLResponse)
def returnErro(request = Request, user_id: dict = Depends(get_current_user)):
    username = takeUsername(user_id)
    
    return templates.TemplateResponse(
        request = request, name = "error.html", context={"username": username}
    )

    
    
    
        





    
    