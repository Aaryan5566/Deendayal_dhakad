import requests
from pyrogram import Client, filters
import random

# ✅ Manually Add Your API Details Here
API_ID = 23378704  # ⚠️ Yaha Apni API ID Dalna
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"  # ⚠️ Yaha Apni API Hash Dalna
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"  # ⚠️ Yaha Apna Bot Token Dalna
OMDB_API_KEY = "223e6df"  # ⚠️ Yaha Apni OMDb API Key Dalna

# ✅ Pyrogram Client Setup
app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ OMDb API Se Trending Movies & Web Series Fetch Karne Ka Function
def get_trending_movies():
    url = f"https://www.omdbapi.com/?s=movie&type=movie&apikey={OMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("Search", [])
        if not movies:
            return "❌ No trending movies found."

        trending_list = []
        for index, movie in enumerate(movies[:5], start=1):  # Sirf Top 5 Movies
            title = movie.get("Title", "Unknown")
            year = movie.get("Year", "N/A")
            imdb_id = movie.get("imdbID", "N/A")
            imdb_link = f"https://www.imdb.com/title/{imdb_id}/"
            
            trending_list.append(f"🎬 **{index}. {title} ({year})**\n🎭 [IMDB Link]({imdb_link})\n")

        return "\n".join(trending_list)
    else:
        return "❌ Error fetching movies."

def get_trending_series():
    url = f"https://www.omdbapi.com/?s=series&type=series&apikey={OMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        series = data.get("Search", [])
        if not series:
            return "❌ No trending web series found."

        trending_list = []
        for index, show in enumerate(series[:5], start=1):  # Sirf Top 5 Series
            title = show.get("Title", "Unknown")
            year = show.get("Year", "N/A")
            imdb_id = show.get("imdbID", "N/A")
            imdb_link = f"https://www.imdb.com/title/{imdb_id}/"
            
            trending_list.append(f"📺 **{index}. {title} ({year})**\n🎭 [IMDB Link]({imdb_link})\n")

        return "\n".join(trending_list)
    else:
        return "❌ Error fetching series."

# ✅ /movies Command Handler
@app.on_message(filters.command("movies"))
async def movies_command(client, message):
    # 🔥 Multiple Reactions
    reactions = ["🔥", "💥", "🤩", "🎬", "🍿"]
    for reaction in reactions:
        await message.react(reaction)

    # 🎭 Custom "Movies ka Baap" Message
    await message.reply_text("🎬 **Movies ka Baap Aa Gaya!** 🍿\n🔍 Fetching trending movies & web series...")

    movies = get_trending_movies()
    series = get_trending_series()

    trending_text = f"🔥 **Trending Movies:**\n{movies}\n\n🎭 **Trending Web Series:**\n{series}"
    
    await message.reply_text(trending_text)

# ✅ Bot Start Karega
app.run()
