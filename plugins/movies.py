import requests
from pyrogram import Client, filters

# Bot & API Configuration
API_ID = 23378704  # Apna API ID daal
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"  # Apna API Hash daal
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"  # Apna bot token daal
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"  # Teri TMDb API key

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

    text = "🎬 **Latest Movies:**\n"
    for i, movie in enumerate(movies, 1):
        text += f"**{i}. {movie['title']}**\n📅 Release Date: {movie['release_date']}\n\n"

    message.reply_text(text)

    # Posters send karna
    for movie in movies:
        if movie["poster"]:
            message.reply_photo(photo=movie["poster"], caption=f"🎬 {movie['title']}\n📅 Release Date: {movie['release_date']}")

if __name__ == "__main__":
    app.run()
