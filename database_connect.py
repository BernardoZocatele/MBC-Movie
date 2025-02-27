import sqlite3
from hashe import check_password
from get_images import get_poster
import requests

def get_poster_path(filmName):
    API_KEY = '9479df05133f28d9fcfae9bf89be7ec0'
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={filmName}"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        if dados['results']:
            film = dados['results'][0]
            poster_path = film['poster_path']

            return poster_path
        else: return {'message': 'Filme nao encontrado'}
    else: return f"Erro na API: {resposta.status_code}"


def connectDB():
    connector = sqlite3.connect('movie.db', check_same_thread=False)
    cursor = connector.cursor()
    
    return cursor, connector

def addUserDb(user):
    connector = sqlite3.connect('movie.db', check_same_thread=False)
    cursor = connector.cursor()
    
    addId = user.user_id
    addUsername = user.username
    addPassword = user.password
    
    cursor.execute(f"insert into users values({addId}, '{addUsername}', '{addPassword}')")
    connector.commit()
    connector.close()
    
def checkId(random_id):
    connector = sqlite3.connect('movie.db', check_same_thread=False)
    cursor = connector.cursor()
    
    cursor.execute("Select id From users")
    user_ids = cursor.fetchall()
    connector.close()
    
    for user_id in user_ids:
        if random_id == user_id:
            return 1 #Falha na operação, id ja existente
    return 0 #sucesso, poassou por todos ids sem encontrar um igual
    

def checkLogin(loginUser, loginPassword):
    cursor, connector = connectDB()
    cursor.execute(f"select password from users where username='{loginUser}'")
    result = cursor.fetchone()
    connector.close()
    
    if not result:
        return 1 # usuario nao encontrado
    
    hashedPassword = result[0]
    
    if check_password(hashedPassword, loginPassword):
        return 0 # senha do usuario válida
    else:
        return 1 # senha incorreta
    
def takeId(loginUser):
    cursor, connector = connectDB()
    cursor.execute(f"Select id from users where username='{loginUser}'")
    result = cursor.fetchone()
    connector.close()
    
    id = result[0]
    return id

def saveMovieDB(movieInfos):
    cursor, connector = connectDB()
    cursor.execute(
        "INSERT INTO movies (id, movie, gender, release) VALUES (?, ?, ?, ?)",
        (movieInfos.user_id, movieInfos.movie, movieInfos.gender, movieInfos.release)
    )
    connector.commit()
    connector.close()

def takeUsername(user_id):
    cursor, connector = connectDB()
    cursor.execute(f"select username from users where id={user_id}")
    result = cursor.fetchone()
    connector.close()
    
    username = result[0]
    
    return username    

def takeMyMovies(user_id: int):
    posters = []
    
    cursor, connector = connectDB()
    cursor.execute(f"Select movie from movies where id={user_id}")
    results = cursor.fetchall()
    
    
    for result in results:
        poster_path = get_poster_path(result)
        posters.append(get_poster(poster_path))
    
    connector.close()
    
    return results, posters
    
def checkSaveMovie(title: str, user_id: int):
    cursor, connector = connectDB()
    cursor.execute(f"select * from movies where movie = ? and id = ?", (title, user_id))
    result = cursor.fetchall()
    
    connector.close()
    
    if result:
        # resultado encontrado, filme ja adicionado como favorito pello usuario
        return 1
    return 0

def createRate(movie, media):
    cursor, connector = connectDB()
    cursor.execute("INSERT INTO rate VALUES (?, ?, ?)", (movie, media, 1))
    connector.commit()
    connector.close()

def updateRate(media, votes, movie):
    mediaRound = round(media,1)
    
    cursor, connector = connectDB()
    cursor.execute("update rate set media = ?, votes = ? where movie = ?", (mediaRound, votes, movie))
    connector.commit()
    connector.close

def takeVotes(movie: str, star: int):
    cursor, connector = connectDB()
    cursor.execute("Select media, votes from rate where movie = ?", (movie, ))
    
    result = cursor.fetchone()
    connector.close()
    
    if result:
        media = result[0]
        votes = result[1]
        temp = media*votes
        votes+=1
        temp+=star
    
        newMedia = temp/votes
        updateRate(newMedia, votes, movie)
        return 0
    else:
        createRate(movie, star)
        return 0

def mediaRate(movie: str):
    cursor, connector = connectDB()
    cursor.execute("select media from rate where movie = ?", (movie, ))
    
    result = cursor.fetchone()
    connector.close()
    if result:
        return result[0]
    else: return 0   
    
def deleteVote(vote, movie):
    cursor, connector = connectDB()
    cursor.execute("Select media, votes from rate where movie = ?", (movie, ))
    results = cursor.fetchone()
    
    temp = float(results[0])*float(results[1])
    temp -= vote
    qtdVotes = results[1] - 1
    
    cursor.execute("update rate set media = ?, votes = ? where movie = ?", (temp, qtdVotes, movie))
    connector.commit()
    connector.close()
    
def checkLastRate(user_id, movie):
    cursor, connector = connectDB()
    cursor.execute("Select rate from movies where id = ? and movie = ?", (user_id, movie))
    result = cursor.fetchone()
    print(result)
    
    connector.close()
    if result[0] != None:
        # jogar para função que apaga o voto antigo e atualiza.
        deleteVote(result[0], movie)
        
def createUserVoteHistory(movie, star, user_id):
    cursor, connector = connectDB()
    cursor.execute("update movies set rate = ? where movie = ? and id = ?", (star, movie, user_id))
    connector.commit()
    connector.close()
        
    