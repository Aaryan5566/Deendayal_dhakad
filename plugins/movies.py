import requests
from pyrogram import Client, filters
import random

# ✅ OMDb API Key (Manually Add Karna)
OMDB_API_KEY = "223e6df"

# ✅ Image Show ON/OFF (True = Image Show, False = Sirf Text)
SHOW_PICS = True  

# ✅ Trending Movies Fetch Karne Ka Function
def get_trending_movies():
    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=trending&type=movie"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("Search", [])

        if not movies:
            return "❌ No trending movies found."

        trending_list = []
        for index, movie in enumerate(movies[:5], start=1):  # ✅ 5 Movies
            title = movie.get("Title", "Unknown")
            language = "🌍 Multiple Languages"
            release_date = movie.get("Year", "N/A")
            imdb_id = movie.get("imdbID")
            imdb_link = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "N/A"
            overview = "📖 No description available (OMDb doesn't provide overview)."
            poster_url = movie.get("Poster", None)

            trending_list.append({
                "index": index,
                "title": title,
                "language": language,
                "release_date": release_date,
                "imdb_link": imdb_link,
                "overview": overview,
                "poster_url": poster_url
            })

        return trending_list
    else:
        return "❌ Error fetching trending movies."

# ✅ /movies Command Handler (Plugins Version)
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    # 🎭 Pehle Multiple Reactions Lagayega
    reactions = ["🤡", "🔥", "🎬", "🍿", "💥", "🎭"]
    for emoji in reactions:
        await message.react(emoji)

    reaction_message = await message.reply_text(
        "🎬 **Movie Ka Baap Aa Gaya! 🍿**\n"
        "🔥 Hold tight... Tracking down the hottest trending movies & web series! 🚀"
    )

    movies = get_trending_movies()

    if isinstance(movies, str):  # ✅ Agar Koi Error Aayi
        await reaction_message.edit_text(f"❌ {movies}")
        return

    for movie in movies:
        caption = (
            f"🎬 **{movie['title']}**\n"
            f"🌍 Language: {movie['language']}\n"
            f"📅 Release Date: {movie['release_date']}\n"
            f"🎭 [IMDB Link]({movie['imdb_link']})\n"
            f"📖 {movie['overview']}"  
        )

        if SHOW_PICS and movie["poster_url"]:  # ✅ Agar SHOW_PICS = True hai toh Image Send Karega
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:  # ✅ Agar SHOW_PICS = False hai toh Sirf Text Send Karega
            await message.reply_text(caption)

    await reaction_message.delete()  # ✅ Pehle Wala Message Hata Dega
