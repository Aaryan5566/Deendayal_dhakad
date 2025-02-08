import requests
import asyncio
import random
from pyrogram import Client, filters

# ✅ API KEYS & SETTINGS (Manually Add Karo)
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"
SHOW_PICS = False  # True = Pics ON, False = Pics OFF

# ✅ Trending Movies & Web Series Fetch Karne Ka Function (Sirf India)
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/all/day?api_key={TMDB_API_KEY}&language=en-US&region=IN"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "❌ Error fetching trending content."

    data = response.json().get("results", [])
    if not data:
        return "❌ No trending movies or web series found."

    trending_list = []
    movies_count, web_series_count = 0, 0

    for item in data:
        if movies_count >= 5 and web_series_count >= 5:
            break

        title = item.get("title") or item.get("name", "Unknown")
        release_date = item.get("release_date") or item.get("first_air_date", "N/A")
        category = "🎬 Movie" if "title" in item else "📺 Web Series"
        imdb_id = item.get("id")
        imdb_link = f"https://www.imdb.com/title/tt{imdb_id}/" if imdb_id else "N/A"
        poster_path = item.get("poster_path")
        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        if category == "🎬 Movie" and movies_count < 5:
            movies_count += 1
            trending_list.append({
                "title": title,
                "release_date": release_date,
                "category": category,
                "imdb_link": imdb_link,
                "poster_url": full_poster_url
            })
        
        elif category == "📺 Web Series" and web_series_count < 5:
            web_series_count += 1
            trending_list.append({
                "title": title,
                "release_date": release_date,
                "category": category,
                "imdb_link": imdb_link,
                "poster_url": full_poster_url
            })

    return trending_list

# ✅ /movies Command Handler
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    # ✅ Multiple Reactions Properly Kaam Karenge
    reactions = ["🔥", "🎬", "🍿", "💥", "🎭"]
    for emoji in reactions:
        await message.react(emoji)
        await asyncio.sleep(0.5)

    # ✅ "Movies Ka Baap!" Message Show 4 Sec Ke Liye
    loading_message = await message.reply_text(
        "🎬 **Movies Ka Baap! 🍿**\n"
        "🔥 Hold tight... Fetching the top trending content from India! 🚀"
    )
    await asyncio.sleep(4)
    await loading_message.delete()

    movies = get_trending_movies()
    if isinstance(movies, str):  # Error Case
        await message.reply_text(f"❌ {movies}")
        return

    for movie in movies:
        caption = (
            f"{movie['category']} **{movie['title']}**\n"
            f"📅 Release Date: {movie['release_date']}\n"
            f"⭐ [IMDB Link]({movie['imdb_link']})\n"
        )

        if SHOW_PICS and movie["poster_url"]:
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:
            await message.reply_text(caption)
