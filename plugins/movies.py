import requests
from pyrogram import Client, filters
import random
from info import OMDB_API_KEY, SHOW_PICS  # ✅ API & Settings `info.py` Se Fetch Karega

# ✅ Trending Movies Fetch Karne Ka Function (OMDb API)
def get_trending_movies():
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=latest&type=movie"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("Search", [])

        if not movies:
            return "❌ No trending movies found."

        trending_list = []
        for index, movie in enumerate(movies[:10], start=1):  # Sirf Top 10 Movies Show Karega
            title = movie.get("Title", "Unknown")
            year = movie.get("Year", "N/A")
            imdb_id = movie.get("imdbID")
            imdb_link = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "N/A"
            poster_url = movie.get("Poster") if movie.get("Poster") and movie.get("Poster") != "N/A" else None

            trending_list.append({
                "index": index,
                "title": title,
                "year": year,
                "imdb_link": imdb_link,
                "poster_url": poster_url
            })

        return trending_list
    else:
        return "❌ Error fetching trending movies."

# ✅ /movies Command Handler (Plugins Version)
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    # 🎭 Pehle Multiple Reaction Lagayega
    reaction_emojis = ["🤡", "🔥", "🎬", "🍿", "👀", "💥"]
    for emoji in reaction_emojis:
        await message.react(emoji)

    reaction_message = await message.reply_text(
        "🎬 **Movie Ka Baap Aa Gaya! 🍿**\n"
        "🔥 Hold tight... Tracking down the hottest trending movies! 🚀"
    )

    movies = get_trending_movies()

    if isinstance(movies, str):  # Agar Koi Error Aayi
        await reaction_message.edit_text(f"❌ {movies}")
        return

    for movie in movies:
        caption = (
            f"🎬 **{movie['title']} ({movie['year']})**\n"
            f"🎭 [IMDB Link]({movie['imdb_link']})\n"
        )

        if SHOW_PICS and movie["poster_url"]:  # ✅ Agar SHOW_PICS = True hai toh Image Send Karega
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:  # ✅ Agar SHOW_PICS = False hai toh Sirf Text Send Karega
            await message.reply_text(caption)

    await reaction_message.delete()  # Pehle Wala Message Hata Dega
