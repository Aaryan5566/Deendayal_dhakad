import requests
import random
import re
import asyncio
from pyrogram import Client, filters

# ✅ TMDb API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Random Emoji Reactions
REACTIONS = ["🔥", "😍", "🤩", "🤡", "👻", "🎬", "🫡", "🍿"]

# ✅ Fetch Movie Information
def get_movie_info(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=en-US"
    response = requests.get(url).json()
    if response.get("results"):
        return response["results"][0]  # First search result
    return None

# ✅ /song Command - Search and provide download link and image
@Client.on_message(filters.command("song"))
async def song_command(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    query = message.text.split(" ", 1)
    if len(query) < 2:
        await message.reply_text("❌ Please provide a song name. Example: `/song Shape of You`")
        return

    msg = await message.reply_text(f"🎶 **Searching for '{query[1]}'... 🍿**")
    await asyncio.sleep(3)

    # Example song search from a site like PagalWorld
    song_url, song_image_url = get_song_data(query[1])
    
    if not song_url:
        await msg.edit_text("❌ Song not found.")
        return

    response_text = f"🎶 **Song:** {query[1]}\n🔗 Download Link: {song_url}"

    if song_image_url:
        await msg.delete()
        song_msg = await client.send_photo(
            chat_id=message.chat.id,
            photo=song_image_url,
            caption=response_text
        )
    else:
        song_msg = await msg.edit_text(response_text)

    await asyncio.sleep(1200)  # 20 minutes (auto-delete)
    await song_msg.delete()

# ✅ Function to fetch song data (download link & image)
def get_song_data(song_name):
    # Here you would integrate scraping or API for a website like PagalWorld
    # For now, it's just a dummy example
    search_url = f"https://www.pagalworld.ai/search?q={song_name}"
    
    # Send GET request to PagalWorld (or any other source)
    response = requests.get(search_url)
    
    if response.status_code == 200:
        # Here we assume you have parsed the HTML and extracted the download link and image URL
        song_url = "https://www.pagalworld.ai/sample-song.mp3"  # Replace with actual link
        song_image_url = "https://www.pagalworld.ai/sample-image.jpg"  # Replace with actual image URL
        return song_url, song_image_url
    return None, None
