import requests
from pyrogram import Client, filters
import random
import time  

# ✅ API Configuration (Manually Add)
API_ID = "23378704"
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Initialize Pyrogram Client (Root)
app = Client("MovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Function: Fetch 20 Upcoming Movies & Web Series
def get_upcoming():
    url_movies = f"https://api.themoviedb.org/3/movie/upcoming?api_key={TMDB_API_KEY}&language=en-US&page=1"
    url_tv = f"https://api.themoviedb.org/3/tv/on_the_air?api_key={TMDB_API_KEY}&language=en-US&page=1"

    movies_response = requests.get(url_movies)
    tv_response = requests.get(url_tv)

    upcoming_list = []

    if movies_response.status_code == 200 and tv_response.status_code == 200:
        movies = movies_response.json()["results"][:10]  # ✅ 10 Upcoming Movies
        tv_shows = tv_response.json()["results"][:10]   # ✅ 10 Upcoming TV Series

        for movie in movies:
            upcoming_list.append({
                "title": movie.get("title", "Unknown"),
                "release_date": movie.get("release_date", "N/A"),
                "language": movie.get("original_language", "N/A").upper(),
                "poster_url": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None
            })

        for show in tv_shows:
            upcoming_list.append({
                "title": show.get("name", "Unknown"),
                "release_date": show.get("first_air_date", "N/A"),
                "language": show.get("original_language", "N/A").upper(),
                "poster_url": f"https://image.tmdb.org/t/p/w500{show['poster_path']}" if show.get("poster_path") else None
            })

        return upcoming_list
    else:
        return "❌ Error fetching upcoming movies & series."

# ✅ /movies Command Handler (Root Version)
@app.on_message(filters.command("movies"))
async def movies_command(client, message):
    reactions = ["😍", "👻", "🫡", "🤩", "🤡"]
    await message.react(random.choice(reactions))

    msg = await message.reply_text("🎬 **Movies Ka Asli Baap Aa Gaya! Hold Tight... 🔥**")
    
    time.sleep(4)
    await msg.delete()

    upcoming = get_upcoming()

    if isinstance(upcoming, str):  # ❌ Agar Koi Error Aaye
        await message.reply_text(upcoming)
        return

    for item in upcoming:
        caption = (
            f"🎬 **{item['title']}**\n"
            f"📅 Release Date: {item['release_date']}\n"
            f"🌍 Language: {item['language']}\n"
        )

        if item["poster_url"]:  # ✅ Agar Poster Hai Toh Image Send Karega
            await client.send_photo(message.chat.id, item["poster_url"], caption=caption)
        else:  # ❌ Agar Poster Nahi Hai Toh Sirf Text Send Karega
            await message.reply_text(caption)

# ✅ Run Bot
app.run()
