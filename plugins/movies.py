import requests
from info import TMDB_API_KEY  

async def get_latest_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        return "Error fetching movies."

    data = response.json()
    movies = data.get("results", [])
    if not movies:
        return "No trending movies found."

    movie_list = []
    for movie in movies[:10]:  
        title = movie.get("title", "Unknown")
        poster_path = movie.get("poster_path")
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        imdb_link = f"https://www.imdb.com/title/{movie.get('imdb_id', '')}"  
        story = movie.get("overview", "No story available.")

        movie_list.append((title, full_poster_url, imdb_link, story))

    return movie_list
