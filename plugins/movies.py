import requests
import asyncio
import random
import re
from pyrogram import Client, filters

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

# ✅ Fetch Movie Information
def get_movie_info(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=en-US"
    response = requests.get(url).json()
    if response.get("results"):
        return response["results"][0]  # First search result
    return None

# ✅ /topmovies Command - Highest IMDb Rated Movies & Web Series
@Client.on_message(filters.command("topmovies"))
async def top_movies_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    msg = await message.reply_text("🎬 **Wait... Top IMDb Movies & Web Series Fetch Kar Raha Hoon! 🍿**")
    await asyncio.sleep(3)

    movies = get_top_imdb_movies()
    tv_shows = get_top_imdb_tv_shows()

    if not movies and not tv_shows:
        await msg.edit_text("❌ No top IMDb movies or web series found.")
        return

    response_text = "**🔥 Top 10 IMDb Movies:**\n\n"
    for index, movie in enumerate(movies, start=1):
        title = movie.get("title", "Unknown")
        release_date = movie.get("release_date", "N/A")
        rating = movie.get("vote_average", "N/A")
        response_text += f"**{index}. {title}**\n⭐ IMDb: {rating}/10\n📅 Release: {release_date}\n\n"

    response_text += "\n**📺 Top 10 IMDb Web Series:**\n\n"
    for index, tv_show in enumerate(tv_shows, start=1):
        title = tv_show.get("name", "Unknown")
        first_air_date = tv_show.get("first_air_date", "N/A")
        rating = tv_show.get("vote_average", "N/A")
        response_text += f"**{index}. {title}**\n⭐ IMDb: {rating}/10\n📅 First Aired: {first_air_date}\n\n"

    top_msg = await msg.edit_text(response_text)
    
    await asyncio.sleep(1200)  # 20 minutes (auto-delete)
    await top_msg.delete()

# ✅ /topmoviesYYYY Command - Top Movies & Web Series of a Specific Year
@Client.on_message(filters.regex(r"^/topmovies(\d{4})$"))
async def top_movies_year_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    year_match = re.match(r"^/topmovies(\d{4})$", message.text)
    if not year_match:
        return

    year = int(year_match.group(1))
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

    await asyncio.sleep(1200)  # 20 minutes (auto-delete)
    await year_msg.delete()

# ✅ /movieinfo Command - Get Movie Details
@Client.on_message(filters.command("movieinfo"))
async def movie_info_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    query = message.text.split(" ", 1)
    if len(query) < 2:
        await message.reply_text("❌ Please provide a movie name. Example: `/movieinfo Inception`")
        return

    msg = await message.reply_text(f"🎬 **Finding details for '{query[1]}'... 🍿**")
    await asyncio.sleep(3)

    movie = get_movie_info(query[1])
    if not movie:
        await msg.edit_text("❌ Movie not found.")
        return

    title = movie.get("title", "Unknown")
    release_date = movie.get("release_date", "N/A")
    rating = movie.get("vote_average", "N/A")
    overview = movie.get("overview", "No overview available.")
    poster_path = movie.get("poster_path")

    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    response_text = f"🎬 **{title}**\n⭐ IMDb: {rating}/10\n📅 Release: {release_date}\n\n📖 **Overview:**\n{overview}"

    if poster_url:
        await msg.delete()
        info_msg = await client.send_photo(
            chat_id=message.chat.id,
            photo=poster_url,
            caption=response_text
        )
    else:
        info_msg = await msg.edit_text(response_text)

    await asyncio.sleep(1200)  # 20 minutes (auto-delete)
    await info_msg.delete()
