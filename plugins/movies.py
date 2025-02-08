import requests
import asyncio
from pyrogram import Client, filters
import random

# ✅ TMDb API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Random Emoji Reactions
REACTIONS = ["🔥", "😍", "🤩", "🤡", "👻", "🎬", "🫡", "🍿"]

# ✅ Fetch Top 10 IMDb Movies
def get_top_imdb_movies(year=None):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by=vote_average.desc&vote_count.gte=1000&language=en-US"
    if year:
        url += f"&primary_release_year={year}"
    response = requests.get(url)
    return response.json().get("results", [])[:10] if response.status_code == 200 else []

# ✅ Fetch Top 10 IMDb Web Series
def get_top_imdb_tv_shows(year=None):
    url = f"https://api.themoviedb.org/3/discover/tv?api_key={TMDB_API_KEY}&sort_by=vote_average.desc&vote_count.gte=500&language=en-US"
    if year:
        url += f"&first_air_date_year={year}"
    response = requests.get(url)
    return response.json().get("results", [])[:10] if response.status_code == 200 else []

# ✅ /topmovies Command - Highest IMDb Rated Movies (Auto-Delete Enabled)
@Client.on_message(filters.command("topmovies"))
async def top_movies_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    msg = await message.reply_text("🎬 **Wait... Tere Liye Top IMDb Movies Dhund Raha Hoon! 🍿**")
    await asyncio.sleep(3)

    movies = get_top_imdb_movies()
    if not movies:
        await msg.edit_text("❌ No top IMDb movies found.")
        return

    response_text = "**🔥 Top 10 Highest IMDb Rated Movies:**\n\n"
    for index, movie in enumerate(movies, start=1):
        title = movie.get("title", "Unknown")
        release_date = movie.get("release_date", "N/A")
        rating = movie.get("vote_average", "N/A")
        response_text += f"**{index}. {title}**\n⭐ IMDb: {rating}/10\n📅 Release: {release_date}\n\n"

    top_msg = await msg.edit_text(response_text)
    
    await asyncio.sleep(600)  # 10 Min Baad Message Delete
    await top_msg.delete()

# ✅ /topmoviesYYYY Command - Top Movies & Web Series of a Specific Year (Auto-Delete Enabled)
@Client.on_message(filters.command(re.compile(r"topmovies(\d{4})")))
async def top_movies_year_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    year = int(message.matches[0].group(1))
    msg = await message.reply_text(f"🎬 **Wait... Top IMDb Movies & Web Series for {year} Fetch Kar Raha Hoon! 🍿**")
    await asyncio.sleep(3)

    movies = get_top_imdb_movies(year)
    tv_shows = get_top_imdb_tv_shows(year)

    response_text = f"**🔥 Top 10 IMDb Movies ({year}):**\n\n"
    for index, movie in enumerate(movies, start=1):
        title = movie.get("title", "Unknown")
        release_date = movie.get("release_date", "N/A")
        rating = movie.get("vote_average", "N/A")
        response_text += f"**{index}. {title}**\n⭐ IMDb: {rating}/10\n📅 Release: {release_date}\n\n"

    response_text += f"\n**📺 Top 10 IMDb Web Series ({year}):**\n\n"
    for index, tv_show in enumerate(tv_shows, start=1):
        title = tv_show.get("name", "Unknown")
        first_air_date = tv_show.get("first_air_date", "N/A")
        rating = tv_show.get("vote_average", "N/A")
        response_text += f"**{index}. {title}**\n⭐ IMDb: {rating}/10\n📅 First Aired: {first_air_date}\n\n"

    year_msg = await msg.edit_text(response_text)

    await asyncio.sleep(600)  # 10 Min Baad Message Delete
    await year_msg.delete()
