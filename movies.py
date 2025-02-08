import requests
import random

# ✅ TMDb API Key (Yaha Apni API Key Dalna)
TMDB_API_KEY = "YOUR_TMDB_API_KEY"

# ✅ Trending Movies Fetch Karne Ka Function
def get_trending_movies(country_code):
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}&language=en-US&region={country_code}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])[:5]  # Sirf Top 5 Movies
        return movies if movies else f"❌ No trending movies found in {country_code}."
    else:
        return f"❌ Error fetching movies for {country_code}."

# ✅ Trending Web Series Fetch Karne Ka Function
def get_trending_web_series(country_code):
    url = f"https://api.themoviedb.org/3/trending/tv/day?api_key={TMDB_API_KEY}&language=en-US&region={country_code}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        web_series = data.get("results", [])[:5]  # Sirf Top 5 Web Series
        return web_series if web_series else f"❌ No trending web series found in {country_code}."
    else:
        return f"❌ Error fetching web series for {country_code}."

# ✅ India + USA Trending Content Fetch Karke Print Karega
def fetch_trending():
    reactions = ["🔥", "🎬", "🍿", "📺", "💥", "⚡", "🚀", "🎭"]
    print(f"{random.choice(reactions)} **Movie Baap OP Aa Gaya! 🍿**\n")

    for country_code, country_name in [("IN", "India 🇮🇳"), ("US", "USA 🇺🇸")]:
        movies = get_trending_movies(country_code)
        web_series = get_trending_web_series(country_code)

        print(f"📌 **{country_name} Trending Movies:**")
        if isinstance(movies, str):
            print(movies)
        else:
            for index, movie in enumerate(movies, start=1):
                title = movie.get("title", "Unknown")
                release_date = movie.get("release_date", "N/A")
                print(f"{index}. **{title}** ({release_date})")

        print(f"\n📺 **{country_name} Trending Web Series:**")
        if isinstance(web_series, str):
            print(web_series)
        else:
            for index, series in enumerate(web_series, start=1):
                title = series.get("name", "Unknown")
                first_air_date = series.get("first_air_date", "N/A")
                print(f"{index}. **{title}** ({first_air_date})")

        print("\n" + "-" * 40 + "\n")

# ✅ Run the function
if __name__ == "__main__":
    fetch_trending()
