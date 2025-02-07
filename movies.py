import requests

def get_latest_movies():
    url = "https://yts.mx/api/v2/list_movies.json?limit=10&sort_by=date_added"
    
    response = requests.get(url)
    if response.status_code != 200:
        return ["Error fetching movies"]

    data = response.json()
    movies = [movie["title"] for movie in data.get("data", {}).get("movies", [])]

    return movies if movies else ["No new movies found."]

def movies_command():
    latest_movies = get_latest_movies()
    return "\\n".join(latest_movies) if latest_movies else "No new movies found."

if __name__ == "__main__":
    print(movies_command())  # Test the script
