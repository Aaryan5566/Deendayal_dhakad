import requests
from pyrogram import Client, filters
import random
import time  

# ✅ API Configuration (Manually Add)
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Function to Fetch Movie Details
def get_movie_info(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])

        if not results:
            return "❌ No movie found with this name."

        movie = results[0]  # First Search Result
        title = movie.get("title", "Unknown")
        release_date = movie.get("release_date", "N/A")
        language = movie.get("original_language", "N/A").upper()
        overview = movie.get("overview", "No description available.")
        imdb_id = movie.get("id")
        imdb_link = f"https://www.imdb.com/title/tt{imdb_id}/" if imdb_id else "N/A"
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        return {
            "title": title,
            "release_date": release_date,
            "language": language,
            "overview": overview,
            "imdb_link": imdb_link,
            "poster_url": poster_url
        }
    else:
        return "❌ Error fetching movie data."

# ✅ /movieinfo Command Handler
@Client.on_message(filters.command("movieinfo"))
async def movie_info_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Please provide a movie name!**\n`Example: /movieinfo Inception`")
        return

    movie_name = " ".join(message.command[1:])  # Extract Movie Name

    # 🎭 Multiple Reactions
    reactions = ["😍", "👻", "🫡", "🤩", "🤡"]
    reaction_emoji = random.choice(reactions)
    await message.react(reaction_emoji)

    # 🎬 Stylish Fetching Message
    fetching_message = await message.reply_text(
        f"🍿 **Hold on! Fetching Movie Information...** 🎥\n\n"
        f"🔍 Searching for `{movie_name}`..."
    )

    movie = get_movie_info(movie_name)

    if isinstance(movie, str):  # If Error
        await fetching_message.edit_text(f"❌ {movie}")
        return

    caption = (
        f"🎬 **{movie['title']}**\n"
        f"📅 Release Date: {movie['release_date']}\n"
        f"🌍 Language: {movie['language']}\n"
        f"📖 {movie['overview'][:300]}...\n"  # 300 Character Summary
        f"🔗 [IMDB Link]({movie['imdb_link']})"
    )

    # ✅ Send Movie Poster if Available
    if movie["poster_url"]:
        await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
    else:
        await message.reply_text(caption)

    await fetching_message.delete()  # Remove Fetching Message
