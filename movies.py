import asyncio
from pyrogram import Client, filters
from info import API_ID, API_HASH, BOT_TOKEN  

app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("🎬 **Welcome to Movies Bot!** Type /movies to see trending movies.")

@app.on_message(filters.command("movies"))
async def movies_command(client, message):
    await message.reply_text("🤡 **Wait! I am finding trending movies...**")  # Reaction

    from plugins.movies import get_latest_movies  
    movies = await get_latest_movies()

    if isinstance(movies, str):  
        await message.reply_text(f"🎬 Latest Movies:\n\n{movies}")
        return

    for title, poster_url, imdb_link, story in movies:
        caption = f"**🎬 {title}**\n🔗 [IMDB]({imdb_link})\n📖 {story}"
        if poster_url:
            await client.send_photo(message.chat.id, poster_url, caption=caption)
        else:
            await message.reply_text(caption)

if __name__ == "__main__":
    app.run()
