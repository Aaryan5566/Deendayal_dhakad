import asyncio
from pyrogram import Client
from plugins.movies import send_movies_to_channel  # Movies Plugin Import Kiya

# ✅ Bot Credentials
API_ID = 23378704
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"

# ✅ Pyrogram Client Initialize
app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def main():
    async with app:
        await send_movies_to_channel()  # ✅ Auto-post chalayega

if __name__ == "__main__":
    app.run(main())  # ✅ Bot Start Karega
