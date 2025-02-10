from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from datetime import datetime, timedelta
import threading
import random

# ✅ Random Reactions
REACTIONS = ["🤡", "🫡", "🥰", "😇"]

# ✅ TMDb API Configuration
TMDB_API_KEY = '2937f761448c84e103d3ea8699d5a33c'
TMDB_API_URL = 'https://api.themoviedb.org/3/search/multi'

# ✅ Admin Channel ID
ADMIN_CHANNEL = '-1002393373626'  # Replace with your channel username or ID

# ✅ Function: Fetch Details from TMDb API
def get_media_details(query):
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'en-US'
    }
    response = requests.get(TMDB_API_URL, params=params).json()

    if 'results' in response and len(response['results']) > 0:
        item = response['results'][0]
        title = item.get('title') or item.get('name', 'N/A')
        overview = item.get('overview', 'No story available.')
        release_date = item.get('release_date') or item.get('first_air_date', 'N/A')
        rating = item.get('vote_average', 'N/A')
        poster_path = item.get('poster_path')

        # ✅ Image URL
        image_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        # ✅ Random Reaction
        reaction = random.choice(REACTIONS)

        details = f"""
{reaction} {reaction} {reaction}

🎬 *Name:* {title}
📅 *Release Date:* {release_date}
⭐ *IMDb Rating:* {rating}
📝 *Story:* {overview}
"""

        return details, image_url
    else:
        return "🚫 No details found!", None

# ✅ /movie_details Command
@Client.on_message(filters.command("movie_details"))
def movie_details(client, message):
    if len(message.command) < 2:
        message.reply_text("❗ Usage: /movie_details <name>")
        return

    query = ' '.join(message.command[1:])
    details, image_url = get_media_details(query)

    # ✅ "Get Movie" Button
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Get Movie", switch_inline_query_current_chat=query)]
    ])

    if image_url:
        sent_message = message.reply_photo(photo=image_url, caption=details, parse_mode='markdown', reply_markup=buttons)
    else:
        sent_message = message.reply_text(details, parse_mode='markdown', reply_markup=buttons)

    # ✅ Auto-delete after 20 minutes
    threading.Timer(1200, lambda: client.delete_messages(chat_id=message.chat.id, message_ids=sent_message.id)).start()

    # ✅ Send User ID to Admin Channel
    user_id = message.from_user.id
    client.send_message(ADMIN_CHANNEL, f"👤 User ID: `{user_id}` used /movie_details for '{query}'", parse_mode='markdown')
