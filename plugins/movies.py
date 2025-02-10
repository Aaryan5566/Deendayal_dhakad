import requests
from pyrogram import Client, filters

# Bot Configuration (Make sure this matches your bot's settings)
API_ID = 123456  # Replace with your API ID
API_HASH = "your_api_hash_here"  # Replace with your API Hash
BOT_TOKEN = "your_bot_token_here"  # Replace with your Bot Token

# Initialize Pyrogram Client
app = Client("MovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# IMDb API URL (Unofficial API for fetching latest movies)
IMDB_API_URL = "https://imdb-api.projects.thetuhin.com/top/new_movies"

# Command to fetch latest movies
@app.on_message(filters.command("movies") & filters.private)
async def fetch_latest_movies(client, message):
    try:
        await message.reply("🔍 Fetching latest movies from IMDb... Please wait!")

        response = requests.get(IMDB_API_URL).json()

        if "data" in response and isinstance(response["data"], list):
            movies_list = response["data"][:10]  # Get top 10 new release movies
            movies_text = "**🎬 Latest IMDb Releases:**\n\n"

            for movie in movies_list:
                title = movie.get("title", "Unknown")
                year = movie.get("year", "N/A")
                rating = movie.get("rating", "N/A")
                movies_text += f"🎥 **{title}** ({year}) - ⭐ {rating}\n"

            await message.reply(movies_text)
        else:
            await message.reply("🚫 Failed to fetch movie data. Try again later!")

    except Exception as e:
        await message.reply(f"❌ Error fetching movies: {e}")

# Run the bot
if __name__ == "__main__":
    print("MovieBot is running...")
    app.run()
