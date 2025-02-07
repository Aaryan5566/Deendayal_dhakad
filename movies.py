import asyncio
from pyrogram import Client
from movies import get_latest_movies

API_ID = 23378704  
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"
CHANNEL_ID = "@newmoviesupdatechannel2"

app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def send_movie_updates():
    while True:
        movies = get_latest_movies()
        if not movies:
            await app.send_message(CHANNEL_ID, "🎬 No new movies found.")
        else:
            for movie in movies:
                caption = f"🎬 **{movie['title']}**\n"
                caption += f"🌍 Language: {movie['language']}\n"
                caption += f"📅 Release Date: {movie['release_date']}\n"
                caption += f"🎭 [IMDB Link](https://www.themoviedb.org/movie/{movie['imdb_id']})\n"
                caption += f"📖 Story: {movie['overview']}"

                if movie["poster_url"]:
                    await app.send_photo(CHANNEL_ID, movie["poster_url"], caption=caption)
                else:
                    await app.send_message(CHANNEL_ID, caption)

        await asyncio.sleep(21600)  # **6 ghante ka wait (6*60*60 seconds)**

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("✅ Bot is running!")

if __name__ == "__main__":
    app.start()
    asyncio.run(send_movie_updates())
