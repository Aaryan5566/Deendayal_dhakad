import os
import requests
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

@Client.on_message(filters.command(['song', 'mp3']) & filters.private)
async def song(client, message):
    query = ' '.join(message.command[1:])
    if not query:
        await message.reply("कृपया गाने का नाम प्रदान करें। उदाहरण: /song हुमनवा मेरे")
        return

    m = await message.reply("आपके गाने की खोज की जा रही है...")

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            await m.edit("कोई परिणाम नहीं मिला। कृपया अन्य कीवर्ड आज़माएं।")
            return

        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{title}.mp3",
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        await m.edit("गाना डाउनलोड किया जा रहा है...")

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        await message.reply_audio(
            audio=f"{title}.mp3",
            title=title,
            performer="YouTube",
            duration=sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration.split(':')))),
            thumb=thumbnail,
            caption=f"{title}\n{link}"
        )

        os.remove(f"{title}.mp3")
        await m.delete()

    except Exception as e:
        await m.edit(f"कुछ गलत हो गया: {e}")
