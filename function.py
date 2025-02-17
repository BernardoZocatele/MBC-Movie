import requests
import random
from database_connect import checkId

API_KEY = '9479df05133f28d9fcfae9bf89be7ec0'

def get_gender(gender_id):
    gender_list = []
    
    for gender in gender_id:
        match gender:
            case 28:
                gender_temp = 'Action'
                gender_list.append(gender_temp)
            case 12:
                gender_temp = 'Adventure'
                gender_list.append(gender_temp)
            case 16:
                gender_temp = 'Animation'
                gender_list.append(gender_temp)
            case 35:
                gender_temp = 'Comedy'
                gender_list.append(gender_temp)
            case 80:
                gender_temp = 'Crime'
                gender_list.append(gender_temp)
            case 99:
                gender_temp = 'Documentary'
                gender_list.append(gender_temp)
            case 18:
                gender_temp = 'Drama'
                gender_list.append(gender_temp)
            case 10751:
                gender_temp = 'Family'
                gender_list.append(gender_temp)
            case 14:
                gender_temp = 'Fantasia'
                gender_list.append(gender_temp)
            case 36:
                gender_temp = 'History'
                gender_list.append(gender_temp)
            case 27:
                gender_temp = 'Horror'
                gender_list.append(gender_temp)
            case 10402:
                gender_temp = 'Music'
                gender_list.append(gender_temp)
            case 9648:
                gender_temp = 'Mistery'
                gender_list.append(gender_temp)
            case 10749:
                gender_temp = 'Romance'
                gender_list.append(gender_temp)
            case 878:
                gender_temp = 'Ficção científica'
                gender_list.append(gender_temp)
            case 10770:
                gender_temp = 'TV Movie'
                gender_list.append(gender_temp)
            case 53:
                gender_temp = 'Thriller'
                gender_list.append(gender_temp)
            case 10752:
                gender_temp = 'Guerra'
                gender_list.append(gender_temp)
            case 37:
                gender_temp = 'Ocidental'
                gender_list.append(gender_temp)
                
    return gender_list


def buscar_filme(nome_filme):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={nome_filme}"
    
    resposta = requests.get(url)
    if resposta.status_code == 200:
        dados = resposta.json()
        if dados['results']:
            filme = dados['results'][0]  # Pega o primeiro resultado
            
            titulo = filme['title']
            sinopse = filme['overview']
            genero = filme['genre_ids']
            release = filme['release_date']
            poster_path = filme['poster_path']
            
            return titulo, sinopse, genero, release, poster_path
            
        else:
            return "Nenhum filme encontrado."
    else:
        return f"Erro na API: {resposta.status_code}"


def popularFilms():
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        temp = response.json()['results']
        filmes = []
        count = 0
        
        for film in temp:
            count += 1
            filmes.append(film)
            
            if count == 20:
                return filmes
    else:
        return 1
    

def create_id():
    random_id = random.randrange(0,10000)
    
    while checkId(random_id) != 0:
        random_id = random.randrange(0,10000)
        # enquanto a verificaçõ falhar, outro id será gerado
    return random_id

def similar_films(id: int, title):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={id}"
    response = requests.get(url)

    if response.status_code == 200:
        temp = response.json()['results']
        films = []
        count = 0
        
        for film in temp:
            if film['title'] != title:
                count+=1
                films.append(film)
            
            if count == 12:
                return films
    else: return 1