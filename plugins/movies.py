import requests
import asyncio
from pyrogram import Client, filters
import random

# ✅ TMDb API Key (Apni API Key Dalna)
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Random Emoji Reactions
REACTIONS = ["🔥", "😍", "🤩", "🤡", "👻", "🎬", "🫡", "🍿"]

# ✅ Fetch Top 10 Highest IMDb Rated Movies
def get_top_imdb_movies():
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by=vote_average.desc&vote_count.gte=1000&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])[:10]  # Sirf Top 10 Movies
        return movies
    return []

# ✅ /topmovies Command - Highest IMDb Rated Movies
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

    await msg.edit_text(response_text)

# ✅ Fetch Movie Info
def get_movie_info(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            movie = data["results"][0]  # First Result
            return movie
    return None

# ✅ /movieinfo Command - Fetch Movie Details
@Client.on_message(filters.command("movieinfo"))
async def movie_info_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    query = message.text.split(" ", 1)
    if len(query) < 2:
        await message.reply_text("❌ Please enter a movie name! Example: `/movieinfo Inception`")
        return

    movie_name = query[1]
    msg = await message.reply_text(f"🎬 **Fetching Movie Information for:** `{movie_name}`...")
    
    movie = get_movie_info(movie_name)
    if not movie:
        await msg.edit_text("❌ Movie not found!")
        return
    
    title = movie.get("title", "Unknown")
    release_date = movie.get("release_date", "N/A")
    rating = movie.get("vote_average", "N/A")
    overview = movie.get("overview", "No description available.")
    poster_path = movie.get("poster_path")
    full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    caption = (
        f"🎬 **{title}**\n"
        f"⭐ IMDb Rating: {rating}/10\n"
        f"📅 Release Date: {release_date}\n"
        f"📖 {overview[:400]}..."  # Sirf 400 Characters Tak Summary
    )

    if full_poster_url:
        movie_msg = await client.send_photo(message.chat.id, full_poster_url, caption=caption)
    else:
        movie_msg = await message.reply_text(caption)

    await msg.delete()  # Pehle Wala Fetching Message Hata Dega
    await asyncio.sleep(600)  # 10 Min Baad Message Delete
    await movie_msg.delete()
