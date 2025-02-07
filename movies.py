import requests
from pyrogram import Client, filters

API_ID = 23378704  # Yaha apna API_ID daalo
API_HASH = "15a02b4d02babeb79e8f328b0ead0c17"  # Yaha apna API_HASH daalo
BOT_TOKEN = "7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI"  # Yaha apna bot token daalo

app = Client("movies_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_latest_movies():
    url = "https://yts.mx/api/v2/list_movies.json?limit=5&sort_by=date_added"
    
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    movies = data.get("data", {}).get("movies", [])

    return [{"title": movie["title"], "poster": movie["medium_cover_image"]} for movie in movies]

@app.on_message(filters.command("movies"))
def send_movies(client, message):
    movies = get_latest_movies()

    if not movies:
        message.reply_text("No new movies found.")
        return

    for i, movie in enumerate(movies, 1):
        caption = f"🎬 {i}. {movie['title']}"
        message.reply_photo(photo=movie["poster"], caption=caption)

if __name__ == "__main__":
    app.run()
