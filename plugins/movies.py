import requests
import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters

# ✅ API Keys
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"
OMDB_API_KEY = "223e6df"

# ✅ Telegram Channel ID
CHANNEL_USERNAME = "newmoviesupdatechannel2"

# ✅ Har Country Ki Movies Fetch Karne Ka Function
def get_latest_movies():
    today = datetime.now().strftime("%Y-%m-%d")
    one_day_ago = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by=release_date.desc&release_date.gte={one_day_ago}&release_date.lte={today}&language=all&page=1&region="
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])

        movie_list = []
        for movie in movies[:10]:  # Top 10 Latest Movies Fetch Karega
            title = movie.get("title", "Unknown")
            poster_path = movie.get("poster_path")
            imdb_id = get_imdb_id(movie.get("id"))
            overview = movie.get("overview", "No description available.")
            release_date = movie.get("release_date", "Unknown Date")
            language = movie.get("original_language", "Unknown").upper()
            country = get_movie_country(movie.get("id"))
            imdb_rating = get_imdb_rating(imdb_id)

            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            movie_list.append({
                "title": title,
                "poster_url": full_poster_url,
                "imdb_id": imdb_id,
                "imdb_rating": imdb_rating,
                "overview": overview,
                "release_date": release_date,
                "language": language,
                "country": country
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

# ✅ Movie Ka Country Fetch Karne Ka Function
def get_movie_country(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        countries = data.get("production_countries", [])
        if countries:
            return ", ".join([country.get("name", "Unknown") for country in countries])
    return "Unknown"

# ✅ /movies Command Ko Handle Karna
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    movies = get_latest_movies()

    if not movies:
        await message.reply_text("🎬 No new movies found in the last 24 hours.")
        return

    for movie in movies:
        caption = f"🎬 **{movie['title']}**\n"
        caption += f"🌍 Language: {movie['language']}\n"
        caption += f"🌎 Country: {movie['country']}\n"
        caption += f"📅 Release Date: {movie['release_date']}\n"
        caption += f"⭐ IMDB Rating: {movie['imdb_rating']}\n"
        caption += f"🎭 [IMDB Link](https://www.imdb.com/title/{movie['imdb_id']})\n"
        caption += f"📖 Story: {movie['overview']}"

        if movie["poster_url"]:
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:
            await message.reply_text(caption)

# ✅ Har 24 Ghante Me Auto Update Channel Pe Bhejne Ka Function
async def send_movies_to_channel():
    while True:
        movies = get_latest_movies()
        if movies:
            for movie in movies:
                caption = f"🎬 **{movie['title']}**\n"
                caption += f"🌍 Language: {movie['language']}\n"
                caption += f"🌎 Country: {movie['country']}\n"
                caption += f"📅 Release Date: {movie['release_date']}\n"
                caption += f"⭐ IMDB Rating: {movie['imdb_rating']}\n"
                caption += f"🎭 [IMDB Link](https://www.imdb.com/title/{movie['imdb_id']})\n"
                caption += f"📖 Story: {movie['overview']}"

                if movie["poster_url"]:
                    await app.send_photo(CHANNEL_USERNAME, movie["poster_url"], caption=caption)
                else:
                    await app.send_message(CHANNEL_USERNAME, caption)
        else:
            await app.send_message(CHANNEL_USERNAME, "❌ No new movies found in the last 24 hours.")

        await asyncio.sleep(86400)  # ✅ 24 Hours (86400 Seconds) Baad Phir Se Run Karega
