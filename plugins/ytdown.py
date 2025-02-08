import os
import random
import subprocess
import urllib.request
from pyrogram import Client, filters

# ✅ Random Emoji Reactions
REACTIONS = ["🔥", "😍", "🤩", "🤡", "👻", "🎬", "🍿", "📥"]

# ✅ Download `yt-dlp` Binary (Agar Exist Nahi Karta)
YTDLP_URL = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
YTDLP_PATH = "yt-dlp"

if not os.path.exists(YTDLP_PATH):
    urllib.request.urlretrieve(YTDLP_URL, YTDLP_PATH)
    os.chmod(YTDLP_PATH, 0o755)

# ✅ /ytdown Command - Download YouTube Videos
@Client.on_message(filters.command("ytdown"))
async def youtube_download(client, message):
    reaction = random.choice(REACTIONS)
    await message.react(reaction)

    query = message.text.split(" ", 1)
    if len(query) < 2:
        await message.reply_text("❌ **Please provide a YouTube link.**\nExample: `/ytdown <youtube-link>`")
        return

    url = query[1]
    msg = await message.reply_text("📥 **Fetching Video Details...**")

    try:
        # ✅ Get Available Video Formats
        cmd = [YTDLP_PATH, "-F", url]
        process = subprocess.run(cmd, capture_output=True, text=True)
        output = process.stdout

        if "resolution" not in output.lower():
            await msg.edit_text("❌ **No downloadable video found.**")
            return

        response_text = "🎬 **Available Video Qualities:**\n\n"
        quality_dict = {}

        for line in output.split("\n"):
            parts = line.split()
            if len(parts) > 2 and parts[0].isdigit():
                itag = parts[0]
                resolution = parts[-1]
                quality_dict[itag] = resolution
                response_text += f"**{itag}** - {resolution}\n"

        response_text += "\n🔹 **Reply with an itag number to download.**"
        await msg.edit_text(response_text)

        # ✅ Wait for user response
        @Client.on_message(filters.text & filters.reply)
        async def itag_response(client, reply_message):
            itag = reply_message.text.strip()
            if itag in quality_dict:
                download_msg = await reply_message.reply_text("📥 **Downloading Video...**")
                
                file_name = f"video_{itag}.mp4"
                cmd = [YTDLP_PATH, "-f", itag, "-o", file_name, url]
                subprocess.run(cmd, capture_output=True, text=True)

                if os.path.exists(file_name):
                    await client.send_video(
                        chat_id=reply_message.chat.id,
                        video=file_name,
                        caption="✅ **Download Complete!**"
                    )
                    os.remove(file_name)
                else:
                    await reply_message.reply_text("❌ **Download failed.**")

                await download_msg.delete()
            else:
                await reply_message.reply_text("❌ **Invalid itag! Please select from the list.**")

    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {str(e)}")
