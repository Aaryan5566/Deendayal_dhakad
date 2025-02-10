from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from datetime import datetime, timedelta
import threading

# ✅ Google API Config
GOOGLE_API_KEY = 'AIzaSyCOU_1R97pHgzDr7JgOhuNgvleFA2Bf0Go'
CX = 'e2478349016e44cc9'

# ✅ Function: Fetch Movie Details from Google API
def get_movie_details(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}+movie+details&key={GOOGLE_API_KEY}&cx={CX}"
    response = requests.get(url).json()

    if 'items' in response:
        item = response['items'][0]
        title = item.get('title', 'N/A')
        snippet = item.get('snippet', 'N/A')
        image = item.get('pagemap', {}).get('cse_image', [{}])[0].get('src', None)
        release_date = datetime.now().strftime("%Y-%m-%d")  # Placeholder
        imdb_rating = "8.5 ⭐"  # Placeholder

        details = f"""
🤡 🥰 😇 🫡

🎬 *Name:* {title}
📅 *Release Date:* {release_date}
⭐ *IMDb Rating:* {imdb_rating}
📝 *Story:* {snippet}
"""
        return details, image
    else:
        return "🚫 Details not found!", None

# ✅ /movie_details Command
@Client.on_message(filters.command("movie_details"))
def movie_details(client, message):
    if len(message.command) < 2:
        message.reply_text("❗ Usage: /movie_details <movie name>")
        return

    query = ' '.join(message.command[1:])
    details, image = get_movie_details(query)

    if image:
        sent_message = message.reply_photo(photo=image, caption=details, parse_mode='markdown')
    else:
        sent_message = message.reply_text(details, parse_mode='markdown')

    # ⏱️ Auto-delete after 20 minutes
    threading.Timer(1200, lambda: client.delete_messages(chat_id=message.chat.id, message_ids=sent_message.id)).start()

# ✅ /watch Command for Trending Movies
@Client.on_message(filters.command("watch"))
def watch(client, message):
    url = f"https://www.googleapis.com/customsearch/v1?q=trending+movies+2025&key={GOOGLE_API_KEY}&cx={CX}"
    response = requests.get(url).json()

    if 'items' in response:
        buttons = []
        for item in response['items'][:5]:
            title = item.get('title')
            buttons.append([InlineKeyboardButton(title, callback_data=title)])

        reply_markup = InlineKeyboardMarkup(buttons)
        message.reply_text('🎥 *Trending Movies:*', reply_markup=reply_markup, parse_mode='markdown')
    else:
        message.reply_text("🚫 No trending movies found.")

# ✅ Button Handler for Details on Click
@Client.on_callback_query()
def button_handler(client, callback_query):
    movie_name = callback_query.data
    details, image = get_movie_details(movie_name)

    if image:
        callback_query.message.reply_photo(photo=image, caption=details, parse_mode='markdown')
    else:
        callback_query.message.reply_text(details, parse_mode='markdown')

# ✅ Daily Auto-Post for New Releases
def schedule_daily_updates(client):
    while True:
        now = datetime.now()
        target_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now > target_time:
            target_time += timedelta(days=1)

        threading.Event().wait((target_time - now).total_seconds())

        url = f"https://www.googleapis.com/customsearch/v1?q=new+movie+releases+today&key={GOOGLE_API_KEY}&cx={CX}"
        response = requests.get(url).json()

        if 'items' in response:
            message = "🎬 *Today's New Releases:*\n"
            for item in response['items'][:5]:
                title = item.get('title')
                snippet = item.get('snippet')
                message += f"\n• *{title}*\n📝 {snippet}\n"

            client.send_message(chat_id="@your_channel_username", text=message, parse_mode='markdown')

# ✅ Start Auto Update Thread
def start_scheduled_updates(client):
    threading.Thread(target=schedule_daily_updates, args=(client,), daemon=True).start()
