import requests
from pyrogram import Client, filters
import random

# ✅ TMDb API Key (Manually Yaha Dalna)
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Image Show ON/OFF (True = Image Show, False = Sirf Text)
SHOW_PICS = True  

# ✅ TMDb se Trending Movies & Web Series Fetch Karna
def get_trending_content(media_type):
    url = f"https://api.themoviedb.org/3/trending/{media_type}/day?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        items = data.get("results", [])

        if not items:
            return "❌ No trending content found."

        trending_list = []
        for index, item in enumerate(items[:5], start=1):  # Sirf Top 5 Movies/Web Series
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
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    # 🎭 Multiple Reaction Emojis
    reaction_emojis = ["🤡", "🔥", "🎬", "🍿", "🚀", "💥"]
    for emoji in random.sample(reaction_emojis, 3):  # 3 Random Reactions
        await message.react(emoji)

    reaction_message = await message.reply_text(
        "🎬 **Movie Ka Baap Aa Gaya! 🍿**\n"
        "🔥 Hold tight... Finding the hottest trending movies & web series! 🚀"
    )

    # ✅ Trending Movies & Web Series Fetch Karna
    trending_movies = get_trending_content("movie")
    trending_web_series = get_trending_content("tv")

    if isinstance(trending_movies, str) or isinstance(trending_web_series, str):  
        await reaction_message.edit_text("❌ Error fetching trending movies or web series.")
        return

    # ✅ Trending Movies Send Karna
    await message.reply_text("🎥 **Top 5 Trending Movies** 🌍")
    for movie in trending_movies:
        caption = (
            f"🎬 **{movie['title']}**\n"
            f"🌍 Language: {movie['language']}\n"
            f"📅 Release Date: {movie['release_date']}\n"
            f"🎭 [IMDB Link]({movie['imdb_link']})\n"
            f"📖 {movie['overview'][:300]}..."  
        )

        if SHOW_PICS and movie["poster_url"]:
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:
            await message.reply_text(caption)

    # ✅ Trending Web Series Send Karna
    await message.reply_text("📺 **Top 5 Trending Web Series** 🌍")
    for series in trending_web_series:
        caption = (
            f"📺 **{series['title']}**\n"
            f"🌍 Language: {series['language']}\n"
            f"📅 Release Date: {series['release_date']}\n"
            f"🎭 [IMDB Link]({series['imdb_link']})\n"
            f"📖 {series['overview'][:300]}..."  
        )

        if SHOW_PICS and series["poster_url"]:
            await client.send_photo(message.chat.id, series["poster_url"], caption=caption)
        else:
            await message.reply_text(caption)

    await reaction_message.delete()  # Pehle Wala Message Hata Dega
