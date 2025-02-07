from pyrogram import Client, filters
from Deendayal_dhakad.movies import movies_command  # movies.py se function import kiya

@Client.on_message(filters.command("movies"))
async def movies_handler(client, message):
    latest_movies = movies_command()
    await message.reply_text(f"🎬 Latest Movies:\n\n{latest_movies}")
