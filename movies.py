import requests
from pyrogram import Client, filters
import random

# ✅ Wikipedia se Trending Movies & Web Series Fetch Karne Ka Function
def get_trending_wikipedia():
    url_movies = "https://en.wikipedia.org/api/rest_v1/page/summary/List_of_highest-grossing_films"
    url_webseries = "https://en.wikipedia.org/api/rest_v1/page/summary/List_of_most-watched_Netflix_originals"

    response_movies = requests.get(url_movies)
    response_webseries = requests.get(url_webseries)

    trending_movies = []
    trending_webseries = []

    if response_movies.status_code == 200:
        data = response_movies.json()
        extract = data.get("extract", "").split("\n")
        trending_movies = extract[:5]  # ✅ Sirf Top 5 Movies

    if response_webseries.status_code == 200:
        data = response_webseries.json()
        extract = data.get("extract", "").split("\n")
        trending_webseries = extract[:5]  # ✅ Sirf Top 5 Web Series

    return trending_movies, trending_webseries

# ✅ /movies Command Handler (Root Version)
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    # 🎭 Pehle Reaction & Message Send Karega
    reaction_emojis = ["🤡", "🔥", "🎬", "🍿", "💥"]
    await message.react(random.choice(reaction_emojis))

    reaction_message = await message.reply_text(
        "🎬 **Movie Ka Baap Aa Gaya! 🍿**\n"
        "🔥 Hold tight... Tracking down the hottest trending movies & web series! 🚀"
    )

    movies, webseries = get_trending_wikipedia()

    if not movies and not webseries:
        await reaction_message.edit_text("❌ No trending movies or web series found.")
        return

    result_text = "**🔥 Trending Movies:**\n"
    for index, movie in enumerate(movies, start=1):
        result_text += f"{index}. {movie}\n"

    result_text += "\n**🎭 Trending Web Series:**\n"
    for index, series in enumerate(webseries, start=1):
        result_text += f"{index}. {series}\n"

    await reaction_message.edit_text(result_text)
    await reaction_message.delete()  # Pehle Wala Message Hata Dega
