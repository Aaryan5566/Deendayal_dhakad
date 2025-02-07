import requests
from pyrogram import Client, filters

# 🔑 TMDb API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# 🎬 **TMDb API se latest movies fetch karna**
def get_latest_movies():
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page=1"
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
            "overview": movie.get("overview", "No description available."),
        }
        for movie in movies[:10]  # Sirf latest 10 movies fetch karega
    ]

# 📌 **/movies Command Handler**
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    movies = get_latest_movies()

    if not movies:
        await message.reply_text("🎬 No new movies found.")
        return

    text = "🎬 **Latest Movies:**\n\n"
    for i, movie in enumerate(movies, 1):
        text += f"**{i}. {movie['title']}**\n📅 Release Date: {movie['release_date']}\n📖 {movie['overview'][:200]}...\n\n"

    await message.reply_text(text)

    # 🖼 Posters bhejna
    for movie in movies:
        if movie["poster"]:
            await message.reply_photo(movie["poster"], caption=f"🎬 {movie['title']}\n📅 Release Date: {movie['release_date']}\n📖 {movie['overview'][:200]}...")
