import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto

# Bot & API Configuration
API_ID = 23378704  # Apna API ID daalo
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"  # Apna API Hash daalo
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"  # Apna bot token daalo
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"  # Teri TMDb API key
CHANNEL_ID = "-1002370420819"  # Apna Telegram channel ID daalo

app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# TMDb API se latest movies fetch karna
def get_latest_movies():
    url = f"https://api.themoviedb.org/3/movie/upcoming?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    movies = data.get("results", [])

    return [
        {
            "title": movie["title"],
            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie["poster_path"] else None,
            "release_date": movie["release_date"],
            "overview": movie["overview"] if movie["overview"] else "No description available",
            "rating": movie.get("vote_average", "N/A"),
        }
        for movie in movies[:5]  # Sirf latest 5 movies fetch karega
    ]

# /movies command ka handler
@app.on_message(filters.command("movies"))
def send_movies(client, message):
    movies = get_latest_movies()

    if not movies:
        message.reply_text("No new movies found.")
        return

    media_group = []
    for movie in movies:
        caption = f"🎬 **{movie['title']}**\n⭐ **IMDB Rating:** {movie['rating']}\n📅 **Release Date:** {movie['release_date']}\n📝 **Story:** {movie['overview']}"
        
        if movie["poster"]:
            media_group.append(InputMediaPhoto(media=movie["poster"], caption=caption))
        else:
            message.reply_text(caption)

    if media_group:
        message.reply_media_group(media_group)

# Har 6 ghante me movies update karne ka function
async def auto_send_movies():
    while True:
        movies = get_latest_movies()
        
        if movies:
            media_group = []
            for movie in movies:
                caption = f"🎬 **{movie['title']}**\n⭐ **IMDB Rating:** {movie['rating']}\n📅 **Release Date:** {movie['release_date']}\n📝 **Story:** {movie['overview']}"
                
                if movie["poster"]:
                    media_group.append(InputMediaPhoto(media=movie["poster"], caption=caption))
                else:
                    await app.send_message(CHANNEL_ID, caption)
            
            if media_group:
                await app.send_media_group(CHANNEL_ID, media_group)
        
        await asyncio.sleep(21600)  # 6 hours ka delay (21600 seconds)

# Bot Start
@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("🎬 Welcome! Use /movies to see the latest movie updates.")

# Background Task Start
@app.on_message(filters.command("start_autoupdate"))
async def start_auto_update(client, message):
    message.reply_text("✅ Auto-movie updates started!")
    asyncio.create_task(auto_send_movies())

if __name__ == "__main__":
    app.run()
