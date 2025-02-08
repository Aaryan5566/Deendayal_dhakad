import requests
from pyrogram import Client, filters
import random

# ✅ OMDb API Key (Yaha Apni API Key Dalna)
OMDB_API_KEY = "223e6df"  

# ✅ Image Show ON/OFF (True = Image Show, False = Sirf Text)
SHOW_PICS = False  

# ✅ Trending Web Series Fetch Karne Ka Function
def get_trending_web_series():
    url = f"https://www.omdbapi.com/?s=series&type=series&apikey={OMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        series = data.get("Search", [])

        if not series:
            return "❌ No trending web series found."

        trending_list = []
        for index, show in enumerate(series[:5], start=1):  # Sirf Top 5 Web Series Show Karega
            title = show.get("Title", "Unknown")
            year = show.get("Year", "N/A")
            imdb_id = show.get("imdbID", "")
            imdb_link = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "N/A"
            poster_url = show.get("Poster") if SHOW_PICS else None

            trending_list.append({
                "index": index,
                "title": title,
                "year": year,
                "imdb_link": imdb_link,
                "poster_url": poster_url
            })

        return trending_list
    else:
        return "❌ Error fetching trending web series."

# ✅ /series Command Handler (Plugins Version)
@Client.on_message(filters.command("series"))
async def series_command(client, message):
    # 🎭 Pehle Reaction & Message Send Karega
    reaction_emojis = ["🔥", "📺", "🎭", "🎥", "⭐"]
    await message.react(random.choice(reaction_emojis))

    reaction_message = await message.reply_text(
        "📺 **Web Series Ka Baap Aa Gaya! 🎭**\n"
        "🔥 Hold tight... Fetching the latest trending web series! 🚀"
    )

    series = get_trending_web_series()

    if isinstance(series, str):  # Agar Koi Error Aayi
        await reaction_message.edit_text(f"❌ {series}")
        return

    for show in series:
        caption = (
            f"📺 **{show['title']}**\n"
            f"📅 Year: {show['year']}\n"
            f"🎭 [IMDB Link]({show['imdb_link']})"
        )

        if SHOW_PICS and show["poster_url"]:  # ✅ Agar SHOW_PICS = True hai toh Image Send Karega
            await client.send_photo(message.chat.id, show["poster_url"], caption=caption)
        else:  # ✅ Agar SHOW_PICS = False hai toh Sirf Text Send Karega
            await message.reply_text(caption)

    await reaction_message.delete()  # Pehle Wala Message Hata Dega
