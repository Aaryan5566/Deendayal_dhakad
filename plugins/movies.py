import requests
import random
import os
from pyrogram import Client, filters
import asyncio

# ✅ Free Music Archive API URL
FMA_API_URL = 'https://freemusicarchive.org/api/3/'

# ✅ Fetch Song Info from Free Music Archive
def get_fma_song_data(song_name):
    search_url = f"{FMA_API_URL}tracks/search/?query={song_name}&limit=1"
    response = requests.get(search_url).json()
    
    if response.get('data'):
        song_data = response['data'][0]
        download_url = song_data['file_url']  # Actual download link
        song_image_url = song_data['album']['artwork_url'] if song_data['album'].get('artwork_url') else None
        return download_url, song_image_url
    return None, None

# ✅ /song Command - Get Song Download Link and Send File Directly
@Client.on_message(filters.command("song"))
async def song_command(client, message):
    reaction = random.choice(["🔥", "😍", "🎬", "🫡", "🍿"])
    await message.react(reaction)

    query = message.text.split(" ", 1)
    if len(query) < 2:
        await message.reply_text("❌ Please provide a song name. Example: `/song Shape of You`")
        return

    msg = await message.reply_text(f"🎶 **Searching for '{query[1]}' on Free Music Archive... 🍿**")
    
    download_url, song_image_url = get_fma_song_data(query[1])

    if not download_url:
        await msg.edit_text("❌ Song not found.")
        return

    response_text = f"🎶 **Song:** {query[1]}"

    try:
        # Download the file
        file_response = requests.get(download_url, stream=True)
        with open("song.mp3", "wb") as file:
            for chunk in file_response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        
        # Send the downloaded file
        await msg.delete()
        song_msg = await client.send_document(
            chat_id=message.chat.id,
            document="song.mp3",
            caption=response_text
        )

        # Optionally, delete the local file after sending
        os.remove("song.mp3")
        
    except Exception as e:
        await msg.edit_text(f"❌ An error occurred: {str(e)}")

    await asyncio.sleep(1200)  # 20 minutes (auto-delete)
    await song_msg.delete()
