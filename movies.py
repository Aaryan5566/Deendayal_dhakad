import requests
from bs4 import BeautifulSoup

def get_latest_movies():
    url = "https://www.imdb.com/movies-coming-soon/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return ["Error fetching movies"]

    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.select(".list_item h4 a")  # IMDB latest selector

    latest_movies = [movie.text.strip() for movie in movies[:10]]  # Top 10 movies
    return latest_movies if latest_movies else ["No new movies found."]

def movies_command():
    latest_movies = get_latest_movies()
    return "\n".join(latest_movies) if latest_movies else "No new movies found."

if __name__ == "__main__":
    print(movies_command())  # Test the script
