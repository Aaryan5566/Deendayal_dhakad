import os
import os
import asyncio
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message

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
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        file_path = ydl.prepare_filename(info['entries'][0])
        file_path = file_path.replace(".webm", ".mp3").replace(".m4a", ".mp3")
        return file_path, info['entries'][0]['title']

# Telegram command handler
@Client.on_message(filters.command("song") & filters.private)
async def song(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply_text("**Usage:** `/song <song name>`")

    msg = await message.reply_text(f"🔍 **Searching for:** `{query}`")
    
    try:
        file_path, title = await download_audio(query)
        await msg.edit_text("📥 **Uploading song...**")

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
        await msg.edit_text(f"❌ **Error:** {e}")
