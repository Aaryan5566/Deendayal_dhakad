import requests
import random
import threading
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ TMDb API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Random Reactions
REACTIONS = ["🤡", "🫡", "🥰", "😇"]

# ✅ Function to Fetch Media Details from TMDb
def get_media_details(query):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url).json()

    if response.get("results"):
        item = response["results"][0]
        title = item.get("title") or item.get("name", "N/A")
        overview = item.get("overview", "No description available.")
        release_date = item.get("release_date") or item.get("first_air_date", "N/A")
        rating = item.get("vote_average", "N/A")
        poster_path = item.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        reaction = random.choice(REACTIONS)
        details = f"""
{reaction} {reaction} {reaction}

🎬 *Name:* {title}
📅 *Release Date:* {release_date}
⭐ *IMDb Rating:* {rating}
📝 *Story:* {overview}
"""

        return details, poster_url
    else:
        return "🚫 No details found!", None

# ✅ /movie_details Command Handler
@Client.on_message(filters.command("movie_details"))
def movie_details(client, message):
    if len(message.command) < 2:
        message.reply_text("❗ Usage: /movie_details <name>")
        return

    query = ' '.join(message.command[1:])
    details, poster_url = get_media_details(query)

    # ✅ "Get Movie" Button
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Get Movie", switch_inline_query_current_chat=query)]
    ])

    if poster_url:
        sent_message = message.reply_photo(photo=poster_url, caption=details, parse_mode='markdown', reply_markup=buttons)
    else:
        sent_message = message.reply_text(details, parse_mode='markdown', reply_markup=buttons)

    # ✅ Auto-delete after 20 minutes
    threading.Timer(1200, lambda: client.delete_messages(chat_id=message.chat.id, message_ids=sent_message.id)).start()
