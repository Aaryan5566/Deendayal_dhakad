import asyncio
from pyrogram import Client
from movies import get_latest_movies

# Bot Configuration
API_ID = 23378704
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"
CHANNEL_ID = "@newmoviesupdatechannel2"  # Apna Telegram Channel ID daalo

app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def send_movies_to_channel():
    while True:
        movies = get_latest_movies()

        if isinstance(movies, str):
            await app.send_message(CHANNEL_ID, f"🎬 **Latest Movies:**\n\n{movies}")
        else:
            for movie in movies:
                caption = f"**🎬 {movie['title']}**\n📅 Release Date: {movie['release_date']}\n⭐ IMDB: {movie['imdb_rating']}\n📖 {movie['overview']}"
                if movie["poster_url"]:
                    await app.send_photo(CHANNEL_ID, movie["poster_url"], caption=caption)
                else:
                    await app.send_message(CHANNEL_ID, caption)

        await asyncio.sleep(21600)  # 6 ghante ka wait (21600 seconds)

@app.on_message()
async def start_bot(client, message):
    if message.text.lower() == "/start":
        await message.reply_text("Hello! Type /movies to get the latest movies.")

if __name__ == "__main__":
    app.start()
    asyncio.run(send_movies_to_channel())
