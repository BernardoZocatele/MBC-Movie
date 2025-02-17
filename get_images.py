def get_poster(poster_path):

    if poster_path:
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return poster_url 
    else:
        return 0
    
    
    