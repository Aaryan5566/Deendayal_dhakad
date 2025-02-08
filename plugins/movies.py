import requests
from pyrogram import Client, filters
import random
import time  

# ✅ API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Function: Trending Movies Fetch
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()["results"][:40]  # Top 40 Trending Movies
        trending_list = []

        for index, movie in enumerate(data, start=1):
            title = movie.get("title", "Unknown")
            release_date = movie.get("release_date", "N/A")
            language = movie.get("original_language", "N/A").upper()
            imdb_id = movie.get("id")
            imdb_link = f"https://www.imdb.com/title/tt{imdb_id}/" if imdb_id else "N/A"

            trending_list.append(f"**{index}. {title}**\n📅 Release Date: {release_date}\n🌍 Language: {language}\n🔗 [IMDB Link]({imdb_link})\n")

        return "\n".join(trending_list)
    else:
        return "❌ Error fetching trending movies."

# ✅ Command: /movies
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    reactions = ["🔥", "🎬", "🍿", "💥", "⚡", "🚀", "🎞"]
    await message.react(random.choice(reactions))

    msg = await message.reply_text("🎬 **Movies Ka Baap Aa Gaya!** 🍿\n🔥 Fetching trending movies...")

    time.sleep(4)
    await msg.delete()

    trending_movies = get_trending_movies()
    await message.reply_text(f"**🔥 40 Trending Movies:**\n\n{trending_movies}")
