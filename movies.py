import requests
from pyrogram import Client, filters

# ✅ API Keys (Manual Entry)
API_ID = 23378704  # Apna API ID
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"  # Apna API Hash
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"  # Apna bot token
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"  # TMDB API key
SEND_POSTERS = True  # 🖼️ Poster Send Karna Hai? True/False

# ✅ Bot Initialization
app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Trending Movies Fetch Karna
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/all/day?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        return "⚠️ Error Fetching Movies!"

    data = response.json()
    movies = data.get("results", [])

    if not movies:
        return "❌ No New Movies Found!"

    trending_list = []
    for movie in movies[:10]:  # Top 10 Movies & Shows
        title = movie.get("title") or movie.get("name", "Unknown")
        language = movie.get("original_language", "Unknown").upper()
        release_date = movie.get("release_date") or movie.get("first_air_date", "N/A")
        overview = movie.get("overview", "No description available.")
        imdb_link = f"https://www.imdb.com/title/{movie.get('id')}"  # IMDB Link

        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path and SEND_POSTERS else None

        trending_list.append({
            "title": title,
            "language": language,
            "release_date": release_date,
            "overview": overview,
            "imdb_link": imdb_link,
            "poster": poster_url
        })

    return trending_list

# ✅ /movies Command Handler
@app.on_message(filters.command("movies"))
async def movies_command(client, message):
    await message.reply_text("🤡 *Wait... Finding Trending Movies!*", quote=True)

    movies = get_trending_movies()
    if isinstance(movies, str):  # If Error
        await message.reply_text(movies)
        return

    text = "🎬 **Trending Movies & Web Series:**\n\n"
    for movie in movies:
        text += f"**🎥 {movie['title']}**\n🌍 Language: {movie['language']}\n📅 Release Date: {movie['release_date']}\n🎭 [IMDB Link]({movie['imdb_link']})\n📖 {movie['overview'][:150]}...\n\n"

    await message.reply_text(text)

    # ✅ Send Posters Separately
    if SEND_POSTERS:
        for movie in movies:
            if movie["poster"]:
                await client.send_photo(message.chat.id, movie["poster"], caption=f"🎬 {movie['title']}\n📅 Release Date: {movie['release_date']}")

# ✅ Start the Bot
if __name__ == "__main__":
    print("🔥 Bot Started Successfully!")
    app.run()
