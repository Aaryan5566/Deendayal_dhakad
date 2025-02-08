import requests
from pyrogram import Client, filters
import random

# ✅ Image Show ON/OFF (True = Image Show, False = Sirf Text)
SHOW_PICS = True  

# ✅ Trending Movies & Web Series Fetch Karne Ka Function (Google Search)
def get_trending_movies():
    search_url = "https://www.google.com/search?q=trending+movies+and+web+series"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        movies = [movie.text for movie in soup.find_all("h3")][:10]  # ✅ Google Se Top 10 Movies/Web Series Fetch Karega

        if not movies:
            return "❌ No trending movies found."

        trending_list = []
        for index, title in enumerate(movies, start=1):
            imdb_link = f"https://www.google.com/search?q={title.replace(' ', '+')}+IMDB"
            trending_list.append({
                "index": index,
                "title": title,
                "language": "🌍 Multiple Languages",
                "release_date": "N/A",
                "imdb_link": imdb_link,
                "overview": "📖 No description available.",
                "poster_url": None
            })

        return trending_list
    else:
        return "❌ Error fetching trending movies."

# ✅ /movies Command Handler (Root Version)
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    # 🎭 Multiple Reactions Lagayega
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
            f"🎭 [IMDB Search]({movie['imdb_link']})\n"
            f"📖 {movie['overview']}"  
        )

        await message.reply_text(caption)

    await reaction_message.delete()  # ✅ Pehle Wala Message Hata Dega
