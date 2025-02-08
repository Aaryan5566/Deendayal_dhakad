import requests
from pyrogram import Client, filters
import random

# ✅ Manually Add API & Bot Details
API_ID = 23378704  # ⚠️ Yahan Apni API ID Dalna
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"  # ⚠️ Yahan Apna API Hash Dalna
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"  # ⚠️ Yahan Apna Bot Token Dalna
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"  # ⚠️ Yahan Apni TMDb API Key Dalna
SHOW_PICS = False  # ✅ True = Images ON, False = Sirf Text

# ✅ Pyrogram Client Setup
app = Client("MovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Trending Movies & Web Series Fetch Karne Ka Function
def get_trending_content(content_type="movie"):
    url = f"https://api.themoviedb.org/3/trending/{content_type}/day?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        content_list = data.get("results", [])

        trending_list = []
        for index, item in enumerate(content_list[:5], start=1):  # ✅ Sirf Top 5 Movies/Web Series Show Karega
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

# ✅ /movies Command Handler
@app.on_message(filters.command("movies"))
async def movies_command(client, message):
    reaction_emoji = random.choice(["🤡", "🔥", "🎬", "🍿", "⚡"])
    await message.react(reaction_emoji)

    reaction_message = await message.reply_text(
        "🎬 **Movie Ka Baap Aa Gaya! 🍿**\n"
        "🔥 Hold tight... Fetching trending movies & web series! 🚀"
    )

    movies = get_trending_content("movie")
    web_series = get_trending_content("tv")

    if isinstance(movies, str) or isinstance(web_series, str):  
        await reaction_message.edit_text("❌ Error fetching trending content.")
        return

    text = "🔥 **Top 5 Trending Movies:**\n\n"
    for movie in movies:
        text += f"🎬 **{movie['title']}**\n🌍 Language: {movie['language']}\n📅 Release Date: {movie['release_date']}\n🎭 [IMDB]({movie['imdb_link']})\n📖 {movie['overview'][:200]}...\n\n"

    text += "🎭 **Top 5 Trending Web Series:**\n\n"
    for series in web_series:
        text += f"📺 **{series['title']}**\n🌍 Language: {series['language']}\n📅 Release Date: {series['release_date']}\n🎭 [IMDB]({series['imdb_link']})\n📖 {series['overview'][:200]}...\n\n"

    await reaction_message.edit_text(text)
    await reaction_message.delete()

# ✅ Bot Start
app.run()
