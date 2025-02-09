import requests
import asyncio
import random
from pyrogram import Client, filters
import re

# ✅ TMDb API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Random Emoji Reactions
REACTIONS = ["🔥", "😍", "🤩", "🤡", "👻", "🎬", "🫡", "🍿"]

# ✅ Fetch Movie Information
def get_movie_info(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=en-US"
    response = requests.get(url).json()
    if response.get("results"):
        return response["results"][0]  # First search result
    return None

# ✅ Fetch Song Data (without download link, only image)
def get_song_data(song_name):
    search_url = f"https://www.pagalworld.ai/search?q={song_name}"
    response = requests.get(search_url)
    if response.status_code == 200:
        song_image_url = "https://www.pagalworld.ai/sample-image.jpg"  # Replace with actual image URL
        return song_image_url
    return None

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

# ✅ /topmovies Command - Highest IMDb Rated Movies & Web Series
@Client.on_message(filters.command("topmovies"))
async def top_movies_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    msg = await message.reply_text("🎬 **Wait... Top IMDb Movies & Web Series Fetch Kar Raha Hoon! 🍿**")
    await asyncio.sleep(3)

    # Fetch top movies and TV shows (Replace with actual logic to fetch data)
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

# ✅ /song Command - Search and provide song details and image
@Client.on_message(filters.command("song"))
async def song_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    query = message.text.split(" ", 1)
    if len(query) < 2:
        await message.reply_text("❌ Please provide a song name. Example: `/song Shape of You`")
        return

    msg = await message.reply_text(f"🎶 **Searching for '{query[1]}'... 🍿**")
    await asyncio.sleep(3)

    # Fetch song data (image)
    song_image_url = get_song_data(query[1])

    if not song_image_url:
        await msg.edit_text("❌ Song not found.")
        return

    response_text = f"🎶 **Song:** {query[1]}"

    # Send image along with song name
    await msg.delete()
    song_msg = await client.send_photo(
        chat_id=message.chat.id,
        photo=song_image_url,
        caption=response_text
    )

    await asyncio.sleep(1200)  # 20 minutes (auto-delete)
    await song_msg.delete()
