import requests
from pyrogram import Client, filters
import random

# ✅ API Credentials Manually Yaha Dalna
API_ID = "23378704"
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Image Show ON/OFF
SHOW_PICS = True  

app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Trending Content Fetch Karna
def get_trending_content(media_type):
    url = f"https://api.themoviedb.org/3/trending/{media_type}/day?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        items = data.get("results", [])

        if not items:
            return "❌ No trending content found."

        trending_list = []
        for index, item in enumerate(items[:5], start=1):
            title = item.get("title") or item.get("name") or "Unknown"
            language = item.get("original_language", "N/A").upper()
            release_date = item.get("release_date") or item.get("first_air_date") or "N/A"
            imdb_id = item.get("id")
            imdb_link = f"https://www.imdb.com/title/tt{imdb_id}/" if imdb_id else "N/A"
            overview = item.get("overview", "No description available.")
            poster_path = item.get("poster_path")
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
        return "❌ Error fetching trending content."

@app.on_message(filters.command("movies"))
async def movies_command(client, message):
    reaction_emojis = ["🤡", "🔥", "🎬", "🍿", "🚀", "💥"]
    for emoji in random.sample(reaction_emojis, 3):
        await message.react(emoji)

    reaction_message = await message.reply_text(
        "🎬 **Movie Ka Baap Aa Gaya! 🍿**\n"
        "🔥 Hold tight... Finding the hottest trending movies & web series! 🚀"
    )

    trending_movies = get_trending_content("movie")
    trending_web_series = get_trending_content("tv")

    if isinstance(trending_movies, str) or isinstance(trending_web_series, str):  
        await reaction_message.edit_text("❌ Error fetching trending movies or web series.")
        return

    await message.reply_text("🎥 **Top 5 Trending Movies** 🌍")
    for movie in trending_movies:
        if SHOW_PICS and movie["poster_url"]:
            await client.send_photo(message.chat.id, movie["poster_url"], caption=movie["title"])
        else:
            await message.reply_text(movie["title"])

    await message.reply_text("📺 **Top 5 Trending Web Series** 🌍")
    for series in trending_web_series:
        await message.reply_text(series["title"])

    await reaction_message.delete()

app.run()
