import requests
from pyrogram import Client, filters
import asyncio
import random

# 🛠️ TMDb API Config
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"
TMDB_URL = "https://api.themoviedb.org/3/trending/all/day"

# 📌 Image Show ON/OFF (True = Image, False = Sirf Text)
SHOW_PICS = False

# 🔥 Multiple Reactions
REACTIONS = ["🔥", "🎬", "🍿", "💥", "🎭"]

# 📽️ Trending Movies & Web Series Fetch Karne Ka Function
def get_trending_movies():
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = requests.get(TMDB_URL, params=params)

    if response.status_code == 200:
        data = response.json().get("results", [])
        
        movies = [m for m in data if m.get("media_type") == "movie"][:5]  # 🎥 Top 5 Movies
        web_series = [w for w in data if w.get("media_type") == "tv"][:5]  # 📺 Top 5 Web Series
        
        return movies, web_series
    return None, None

# 🎬 /movies Command Handler
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    await message.react(random.choice(REACTIONS))  # 🔥 Random Reaction

    # ⏳ "Movies ka Baap!" Message
    banner_message = await message.reply_text("🎬 **Movies ka Baap! 🍿🔥**\n_Looking for the latest trending movies & web series..._")
    await asyncio.sleep(4)  # ⏳ 4 Sec Delay
    await banner_message.delete()

    # 🎥 Trending Movies & Web Series Fetch Karna
    movies, web_series = get_trending_movies()
    
    if not movies and not web_series:
        await message.reply_text("❌ _Failed to fetch trending movies._")
        return

    # 📌 Trending Movies
    trending_text = "**🔥 Trending Movies:**\n"
    for index, movie in enumerate(movies, start=1):
        title = movie.get("title", "Unknown")
        language = movie.get("original_language", "N/A").upper()
        release_date = movie.get("release_date", "N/A")
        imdb_link = f"https://www.imdb.com/title/tt{movie.get('id')}/"
        trending_text += f"\n**{index}. {title}**\n📅 {release_date} | 🌍 {language} | 🎭 [IMDB]({imdb_link})\n"

    # 📺 Trending Web Series
    trending_text += "\n**📺 Trending Web Series:**\n"
    for index, series in enumerate(web_series, start=1):
        title = series.get("name", "Unknown")
        language = series.get("original_language", "N/A").upper()
        release_date = series.get("first_air_date", "N/A")
        imdb_link = f"https://www.imdb.com/title/tt{series.get('id')}/"
        trending_text += f"\n**{index}. {title}**\n📅 {release_date} | 🌍 {language} | 🎭 [IMDB]({imdb_link})\n"

    await message.reply_text(trending_text)
