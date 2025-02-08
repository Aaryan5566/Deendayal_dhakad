import requests
import asyncio
import random
from pyrogram import Client, filters

# ✅ TMDb API Key (Yaha Apni API Key Dalna)
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Image Show ON/OFF (True = Image Show, False = Sirf Text)
SHOW_PICS = True  

# ✅ Trending Movies Fetch Karne Ka Function
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/all/day?api_key={TMDB_API_KEY}&language=en-IN"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])

        if not movies:
            return "❌ No trending movies found."

        trending_list = []
        for index, movie in enumerate(movies[:5], start=1):  # Sirf Top 5 Movies Show Karega
            title = movie.get("title") or movie.get("name") or "Unknown"
            language = movie.get("original_language", "N/A").upper()
            release_date = movie.get("release_date") or movie.get("first_air_date") or "N/A"
            imdb_id = movie.get("id")
            imdb_link = f"https://www.imdb.com/title/tt{imdb_id}/" if imdb_id else "N/A"
            overview = movie.get("overview", "No description available.")
            poster_path = movie.get("poster_path")
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            trending_list.append({
                "index": index,
                "title": title,
                "language": language,
                "release_date": release_date,
                "imdb_link": imdb_link,
                "overview": overview,
                "poster_url": full_poster_url
            })

        return trending_list
    else:
        return "❌ Error fetching trending movies."

# ✅ /movies Command Handler (Plugins Version)
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    # 🎭 Multiple Reactions
    reaction_emojis = ["🔥", "🎬", "🍿", "🚀"]
    await message.react(random.choice(reaction_emojis))

    # 🎬 "Movies Ka Baap" Message 4 sec tak show karega
    reaction_message = await message.reply_text("🎬 **Movies Ka Baap Aa Gaya!** 🍿")
    await asyncio.sleep(4)
    await reaction_message.delete()

    movies = get_trending_movies()

    if isinstance(movies, str):  # Agar Koi Error Aayi
        await message.reply_text(f"❌ {movies}")
        return

    for movie in movies:
        caption = (
            f"🎬 **{movie['title']}**\n"
            f"🌍 Language: {movie['language']}\n"
            f"📅 Release Date: {movie['release_date']}\n"
            f"🎭 [IMDB Link]({movie['imdb_link']})\n"
            f"📖 {movie['overview'][:300]}..."  # Sirf 300 Characters Ki Summary
        )

        if SHOW_PICS and movie["poster_url"]:  # ✅ Agar SHOW_PICS = True hai toh Image Send Karega
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:  # ✅ Agar SHOW_PICS = False hai toh Sirf Text Send Karega
            await message.reply_text(caption)
