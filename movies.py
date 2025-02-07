import requests
from bs4 import BeautifulSoup

def get_latest_movies():
    url = "https://www.imdb.com/movies-in-theaters/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return ["Error fetching movies"]

    soup = BeautifulSoup(response.text, "html.parser")
    
    movies = []
    for item in soup.select(".ipc-poster-card__title"):
        title = item.get_text(strip=True)
        movies.append(title)

    return movies[:10] if movies else ["No new movies found."]

def movies_command():
    latest_movies = get_latest_movies()
    return "\\n".join(latest_movies) if latest_movies else "No new movies found."

if __name__ == "__main__":
    print(movies_command())  # Test the script
