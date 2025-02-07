import requests
from bs4 import BeautifulSoup

def get_latest_movies():
    url = "https://www.imdb.com/movies-in-theaters/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return ["Error fetching movies"]

    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.select(".list.detail .overview-top a")

    latest_movies = [movie.text.strip() for movie in movies[:10]]  # Top 10 movies
    return latest_movies

def movies_command():
    latest_movies = get_latest_movies()
    return "\n".join(latest_movies) if latest_movies else "No new movies found."

if __name__ == "__main__":
    print(movies_command())  # Test the script
