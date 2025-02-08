import requests
from pyrogram import Client, filters
import random

# ✅ TMDb API Key (Yaha Apni API Key Dalna)
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

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

# ✅ /trending Command Handler (Movies + Web Series for India & USA)
@Client.on_message(filters.command("trending"))
async def trending_command(client, message):
    reactions = ["🔥", "🎬", "🍿", "📺", "💥", "⚡", "🚀", "🎭"]
    await message.react(random.choice(reactions))

    reaction_message = await message.reply_text(
        f"🔥 **Movie Baap OP Aa Gaya! 🍿**\n"
        f"🚀 Fetching Top 5 Trending Movies & Web Series from **India 🇮🇳 & USA 🇺🇸**..."
    )

    # ✅ Fetch India Trending Movies & Web Series
    india_movies = get_trending_movies("IN")
    india_web_series = get_trending_web_series("IN")

    india_movies_text = "**🇮🇳 India Trending Movies:**\n"
    if isinstance(india_movies, str):
        india_movies_text += india_movies
    else:
        for index, movie in enumerate(india_movies, start=1):
            title = movie.get("title", "Unknown")
            release_date = movie.get("release_date", "N/A")
            india_movies_text += f"{index}. **{title}** ({release_date})\n"

    india_web_series_text = "**📺 India Trending Web Series:**\n"
    if isinstance(india_web_series, str):
        india_web_series_text += india_web_series
    else:
        for index, series in enumerate(india_web_series, start=1):
            title = series.get("name", "Unknown")
            first_air_date = series.get("first_air_date", "N/A")
            india_web_series_text += f"{index}. **{title}** ({first_air_date})\n"

    # ✅ Fetch USA Trending Movies & Web Series
    usa_movies = get_trending_movies("US")
    usa_web_series = get_trending_web_series("US")

    usa_movies_text = "**🇺🇸 USA Trending Movies:**\n"
    if isinstance(usa_movies, str):
        usa_movies_text += usa_movies
    else:
        for index, movie in enumerate(usa_movies, start=1):
            title = movie.get("title", "Unknown")
            release_date = movie.get("release_date", "N/A")
            usa_movies_text += f"{index}. **{title}** ({release_date})\n"

    usa_web_series_text = "**📺 USA Trending Web Series:**\n"
    if isinstance(usa_web_series, str):
        usa_web_series_text += usa_web_series
    else:
        for index, series in enumerate(usa_web_series, start=1):
            title = series.get("name", "Unknown")
            first_air_date = series.get("first_air_date", "N/A")
            usa_web_series_text += f"{index}. **{title}** ({first_air_date})\n"

    await message.reply_text(
        f"{india_movies_text}\n\n{india_web_series_text}\n\n{usa_movies_text}\n\n{usa_web_series_text}"
    )
    await reaction_message.delete()
