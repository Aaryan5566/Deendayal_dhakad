import requests
import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters

# ✅ API Keys
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"
OMDB_API_KEY = "223e6df"
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"
API_ID = 23378704
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"

# ✅ Telegram Channel ID (Apne Channel Ka Username @ hata ke likho)
CHANNEL_USERNAME = "newmoviesupdatechannel2"

app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_latest_movies():
    today = datetime.now().strftime("%Y-%m-%d")
    two_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by=release_date.desc&release_date.gte={two_days_ago}&release_date.lte={today}&language=en&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])

        movie_list = []
        for movie in movies[:10]:  # ✅ Sirf Top 10 Movies Show Karega
            title = movie.get("title", "Unknown")
            poster_path = movie.get("poster_path")
            imdb_id = get_imdb_id(movie.get("id"))
            overview = movie.get("overview", "No description available.")
            release_date = movie.get("release_date", "Unknown Date")
            language = movie.get("original_language", "Unknown").upper()
            imdb_rating = get_imdb_rating(imdb_id)

            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            movie_list.append({
                "title": title,
                "poster_url": full_poster_url,
                "imdb_id": imdb_id,
                "imdb_rating": imdb_rating,
                "overview": overview,
                "release_date": release_date,
                "language": language
            })

        return movie_list
    return []

# ✅ IMDB ID Fetch Karne Ka Function
def get_imdb_id(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("imdb_id", "N/A")
    return "N/A"

# ✅ IMDB Rating Fetch Karne Ka Function
def get_imdb_rating(imdb_id):
    if imdb_id == "N/A":
        return "Not Available"
    
    url = f"https://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("imdbRating", "N/A")
    return "N/A"

# ✅ /movies Command Ko Handle Karna
@app.on_message(filters.command("movies"))
async def movies_command(client, message):
    movies = get_latest_movies()

    if not movies:
        await message.reply_text("🎬 No new movies found in the last 2 days.")
        return

    for movie in movies:
        caption = f"🎬 **{movie['title']}**\n"
        caption += f"🌍 Language: {movie['language']}\n"
        caption += f"📅 Release Date: {movie['release_date']}\n"
        caption += f"⭐ IMDB Rating: {movie['imdb_rating']}\n"
        caption += f"🎭 [IMDB Link](https://www.imdb.com/title/{movie['imdb_id']})\n"
        caption += f"📖 Story: {movie['overview']}"

        if movie["poster_url"]:
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:
            await message.reply_text(caption)

# ✅ Har 6 Ghante Me Auto Update Channel Pe Bhejne Ka Function
async def send_movies_to_channel():
    while True:
        movies = get_latest_movies()
        if movies:
            for movie in movies:
                caption = f"🎬 **{movie['title']}**\n"
                caption += f"🌍 Language: {movie['language']}\n"
                caption += f"📅 Release Date: {movie['release_date']}\n"
                caption += f"⭐ IMDB Rating: {movie['imdb_rating']}\n"
                caption += f"🎭 [IMDB Link](https://www.imdb.com/title/{movie['imdb_id']})\n"
                caption += f"📖 Story: {movie['overview']}"

                if movie["poster_url"]:
                    await app.send_photo(CHANNEL_USERNAME, movie["poster_url"], caption=caption)
                else:
                    await app.send_message(CHANNEL_USERNAME, caption)
        else:
            await app.send_message(CHANNEL_USERNAME, "❌ No new movies found in the last 2 days.")

        await asyncio.sleep(21600)  # ✅ 6 Hours (21600 Seconds) Baad Phir Se Run Karega

# ✅ Main Function
async def main():
    async with app:
        await send_movies_to_channel()

if __name__ == "__main__":
    app.run(main())
