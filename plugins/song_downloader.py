import os
import asyncio
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message

# डाउनलोड्स फोल्डर बना दो
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# YouTube से ऑडियो डाउनलोड करने का function
async def download_audio(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320"
        }],
        "quiet": True
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            file_path = ydl.prepare_filename(info['entries'][0])
            file_path = file_path.replace(".webm", ".mp3").replace(".m4a", ".mp3")
            return file_path, info['entries'][0]['title']
    except Exception as e:
        return None, str(e)

# Telegram command handler
@Client.on_message(filters.command("song") & filters.private)
async def song(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("**Usage:** `/song <song name>`")

    msg = await message.reply_text(f"🔍 **Searching for:** `{query}`")
    
    file_path, title = await download_audio(query)

    if not file_path:
        return await msg.edit_text(f"❌ **Download Failed:** {title}")

    await msg.edit_text("📥 **Uploading song...**")

    try:
        await message.reply_audio(
            audio=file_path,
            title=title,
            performer="YouTube",
            caption=f"🎵 **Title:** {title}",
            duration=0
        )

        os.remove(file_path)  # डाउनलोड की हुई फाइल डिलीट कर दें
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ **Upload Error:** {e}")
