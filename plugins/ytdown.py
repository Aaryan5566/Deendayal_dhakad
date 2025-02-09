import asyncio
import random
import yt_dlp
from pyrogram import Client, filters

# ✅ Random Emoji Reactions
REACTIONS = ["🔥"]

# ✅ YouTube Video Downloader Command
@Client.on_message(filters.command("ytdown"))
async def youtube_download(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    if len(message.command) < 2:
        await message.reply_text("❌ **YouTube link do!**\nExample: `/ytdown https://youtu.be/dQw4w9WgXcQ`")
        return

    url = message.command[1]
    msg = await message.reply_text("🔍 **Checking available qualities...**")

    try:
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])

        if not formats:
            await msg.edit_text("❌ No available formats found!")
            return

        format_list = []
        for fmt in formats:
            if fmt.get("ext") == "mp4" and fmt.get("filesize"):
                format_list.append(f"{fmt['format_id']} - {fmt['resolution']} ({round(fmt['filesize'] / (1024 * 1024), 2)} MB)")

        if not format_list:
            await msg.edit_text("❌ No MP4 formats available!")
            return

        quality_text = "**🎬 Available Qualities:**\n" + "\n".join(format_list)
        quality_text += "\n\n**⚡ Select Quality:** `/ytdown <format_id> <YouTube Link>`"
        await msg.edit_text(quality_text)

    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {e}")

# ✅ Download Selected Quality
@Client.on_message(filters.command("ytdown"))
async def youtube_download_selected(client, message):
    if len(message.command) < 3:
        return

    format_id = message.command[1]
    url = message.command[2]
    msg = await message.reply_text("📥 **Downloading... Please wait!**")

    try:
        ydl_opts = {
            "format": format_id,
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await message.reply_video(file_path, caption="✅ **Here is your video!**")
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {e}")
