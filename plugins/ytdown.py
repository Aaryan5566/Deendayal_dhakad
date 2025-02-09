import asyncio
import yt_dlp
from pyrogram import Client, filters

@Client.on_message(filters.command("ytdown"))
async def youtube_download(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Please provide a YouTube video link.**\nExample: `/ytdown https://youtu.be/dQw4w9WgXcQ`")
        return

    url = message.command[1]
    msg = await message.reply_text("🔍 **Fetching video details...**")

    ydl_opts = {"quiet": True, "no_warnings": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])

        buttons = []
        for f in formats:
            if f.get("format_id") and f.get("ext") in ["mp4", "mkv", "webm"]:
                buttons.append((f"🎥 {f['format_note']} ({f['ext']})", f['format_id']))

        if not buttons:
            await msg.edit("❌ No suitable formats found.")
            return

        format_text = "\n".join([f"🎥 `{btn[1]}` - {btn[0]}" for btn in buttons])
        await msg.edit(f"📥 **Available Formats:**\n\n{format_text}\n\n📝 **Reply with the format ID to download.**")

        def check_reply(_, reply):
            return reply.reply_to_message and reply.reply_to_message.message_id == msg.message_id

        reply = await client.listen(message.chat.id, filters=filters.text & filters.user(message.from_user.id), timeout=30)

        format_id = reply.text.strip()
        selected_format = next((f for f in formats if f.get("format_id") == format_id), None)

        if not selected_format:
            await message.reply_text("❌ Invalid format ID selected.")
            return

        await msg.edit(f"⏳ **Downloading... ({selected_format['format_note']})**")

        ydl_opts.update({
            "format": format_id,
            "outtmpl": "downloads/%(title)s.%(ext)s"
        })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        filename = f"downloads/{info['title']}.{selected_format['ext']}"
        await client.send_video(message.chat.id, filename, caption=f"✅ **Downloaded:** {info['title']}")
        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ **Error:** {str(e)}")
