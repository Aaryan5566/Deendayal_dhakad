from pyrogram import Client, filters
import random

# 🎬 Manually Trending Movies & Web Series List
TRENDING_MOVIES = [
    {
        "title": "Dune: Part Two",
        "language": "English",
        "release_date": "2024-03-01",
        "imdb_link": "https://www.imdb.com/title/tt15239678/",
        "overview": "Paul Atreides unites with Chani and the Fremen while seeking revenge against those who destroyed his family."
    },
    {
        "title": "Joker: Folie à Deux",
        "language": "English",
        "release_date": "2024-10-04",
        "imdb_link": "https://www.imdb.com/title/tt11389872/",
        "overview": "A sequel to the 2019 film 'Joker' exploring the complicated relationship between Arthur Fleck and Harley Quinn."
    }
]

TRENDING_WEB_SERIES = [
    {
        "title": "Squid Game: Season 2",
        "language": "Korean",
        "release_date": "2024",
        "imdb_link": "https://www.imdb.com/title/tt10919420/",
        "overview": "The deadly survival game returns with new contestants and even deadlier challenges."
    },
    {
        "title": "House of the Dragon: Season 2",
        "language": "English",
        "release_date": "2024",
        "imdb_link": "https://www.imdb.com/title/tt11198330/",
        "overview": "The Targaryen civil war, the Dance of the Dragons, continues in Westeros."
    }
]

# ✅ /movies Command Handler (Plugin Version)
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    # 🎭 Multiple Reactions
    reactions = ["🔥", "🎬", "🍿", "💥"]
    await message.react(random.choice(reactions))

    reaction_message = await message.reply_text(
        "🔥 **Movies Ka Baap Aa Gaya!** 🍿\n"
        "🎬 Finding the latest trending movies & web series... 🚀"
    )

    msg_text = "🔥 **Trending Movies:**\n"
    for movie in TRENDING_MOVIES:
        msg_text += f"🎬 **{movie['title']}**\n"
        msg_text += f"🌍 Language: {movie['language']}\n"
        msg_text += f"📅 Release Date: {movie['release_date']}\n"
        msg_text += f"🎭 [IMDB Link]({movie['imdb_link']})\n"
        msg_text += f"📖 {movie['overview'][:200]}...\n\n"

    msg_text += "\n🎭 **Trending Web Series:**\n"
    for series in TRENDING_WEB_SERIES:
        msg_text += f"📺 **{series['title']}**\n"
        msg_text += f"🌍 Language: {series['language']}\n"
        msg_text += f"📅 Release Date: {series['release_date']}\n"
        msg_text += f"🎭 [IMDB Link]({series['imdb_link']})\n"
        msg_text += f"📖 {series['overview'][:200]}...\n\n"

    await reaction_message.edit_text(msg_text)
