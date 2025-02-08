import requests
import asyncio
from pyrogram import Client, filters
import random

# ✅ API KEYS & SETTINGS (Manually Add Karo)
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"
OMDB_API_KEY = "223e6df"
BOT_API_ID = 23378704
BOT_API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"

# ✅ MULTIPLE REACTIONS
REACTIONS = ["😍", "👻", "🫡", "🤩", "🤡", "🔥"]

# ✅ MOVIE INFO FETCH KARNE KA FUNCTION
def get_movie_info(movie_name):
    url = f"https://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["Response"] == "True":
            title = data["Title"]
            release_date = data["Released"]
            imdb_rating = data["imdbRating"]
            actors = data["Actors"]
            country = data["Country"]
            plot = data["Plot"]
            return f"🎬 **{title}**\n📅 Release Date: {release_date}\n⭐ IMDb: {imdb_rating}\n🌍 Country: {country}\n🎭 Actors: {actors}\n📖 {plot[:250]}..."
    return "❌ Movie not found."

# ✅ TOP MOVIES BY IMDb RATING FETCH KARNE KA FUNCTION
def get_top_movies():
    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])[:10]  # Top 10 Movies
        top_movies = []
        for movie in movies:
            title = movie.get("title", "Unknown")
            release_date = movie.get("release_date", "N/A")
            imdb_rating = movie.get("vote_average", "N/A")
            top_movies.append(f"🎬 **{title}**\n📅 Release Date: {release_date}\n⭐ IMDb: {imdb_rating}\n")
        return top_movies
    return ["❌ Error fetching top movies."]

# ✅ /movieinfo COMMAND (MOVIE DETAILS WITH AUTO-DELETE)
@Client.on_message(filters.command("movieinfo"))
async def movieinfo_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    movie_name = " ".join(message.command[1:])
    if not movie_name:
        await message.reply_text("❌ Please provide a movie name. Example: `/movieinfo Inception`")
        return

    fetching_msg = await message.reply_text(f"🎬 **Fetching info for:** `{movie_name}`...\n🔍 Please wait...")

    movie_details = get_movie_info(movie_name)
    await fetching_msg.delete()
    movie_message = await message.reply_text(movie_details)

    # ✅ 10 Minutes Ke Baad Delete Ho Jayega
    await asyncio.sleep(600)
    await movie_message.delete()

# ✅ /topmovies COMMAND (TOP MOVIES WITH OP STYLE MESSAGE)
@Client.on_message(filters.command("topmovies"))
async def topmovies_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    fetching_msg = await message.reply_text("🎬 **Wait! Tere Liye Top Movies Dhoond Ke La Raha Hoon...🔥🔥🔥**")

    top_movies = get_top_movies()
    await fetching_msg.delete()
    for movie in top_movies:
        await message.reply_text(movie)

# ✅ TELEGRAM CLIENT SETUP
bot = Client("PlungingMovieBot", api_id=BOT_API_ID, api_hash=BOT_API_HASH, bot_token=BOT_TOKEN)

print("✅ Plunging Movie Bot is Running...")
bot.run()
