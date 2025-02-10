import requests
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from datetime import datetime, timedelta
import threading
import time

# Telegram Bot Token aur Google API Key
BOT_TOKEN = '7917351134:AAFz-wi0zC0PabOOPcWIydblZmkd51WYjWI'
GOOGLE_API_KEY = 'AIzaSyCOU_1R97pHgzDr7JgOhuNgvleFA2Bf0Go'
CX = 'e2478349016e44cc9'  # Google Custom Search Engine ID
CHANNEL_ID = '-1002393373626'  # Telegram channel ID

# ✅ Function: Get Movie/Series/TV Show Details using Google API
def get_movie_details(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}+movie+details&key={GOOGLE_API_KEY}&cx={CX}"
    response = requests.get(url).json()

    if 'items' in response:
        item = response['items'][0]
        pagemap = item.get('pagemap', {})

        title = item.get('title', 'N/A')
        snippet = item.get('snippet', 'N/A')
        image = pagemap.get('cse_image', [{}])[0].get('src', None)
        release_date = datetime.now().strftime("%Y-%m-%d")  # Placeholder
        imdb_rating = "8.5 ⭐"  # Placeholder (you can enhance this)

        details = f"""
🤡 🥰 😇 🫡

*🎬 Name:* {title}
*📅 Release Date:* {release_date}
*⭐ IMDb Rating:* {imdb_rating}
*📝 Story:* {snippet}
"""
        return details, image
    else:
        return "🚫 Details not found!", None

# ✅ /movie_details Command
def movie_details(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("❗ Usage: /movie_details <movie/web series/TV show name>")
        return

    query = ' '.join(context.args)
    details, image = get_movie_details(query)

    if image:
        message = update.message.reply_photo(photo=image, caption=details, parse_mode='Markdown')
    else:
        message = update.message.reply_text(details, parse_mode='Markdown')

    # ⏱️ Auto-delete after 20 minutes
    threading.Timer(1200, lambda: context.bot.delete_message(chat_id=update.message.chat_id, message_id=message.message_id)).start()

# ✅ Function: Get Trending Movies (Google API Based)
def get_trending_movies():
    url = f"https://www.googleapis.com/customsearch/v1?q=trending+movies+2025&key={GOOGLE_API_KEY}&cx={CX}"
    response = requests.get(url).json()

    trending_list = []
    if 'items' in response:
        for item in response['items'][:5]:  # Top 5 trending movies
            title = item.get('title')
            trending_list.append(title)
    return trending_list

# ✅ /watch Command
def watch(update: Update, context: CallbackContext):
    trending_movies = get_trending_movies()

    if not trending_movies:
        update.message.reply_text("🚫 No trending movies found at the moment.")
        return

    keyboard = [[InlineKeyboardButton(movie, callback_data=movie)] for movie in trending_movies]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('🎥 *Trending Movies & Series:*', reply_markup=reply_markup, parse_mode='Markdown')

# ✅ Button Click Handler
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    movie_name = query.data
    details, image = get_movie_details(movie_name)

    if image:
        query.message.reply_photo(photo=image, caption=details, parse_mode='Markdown')
    else:
        query.message.reply_text(details, parse_mode='Markdown')

# ✅ Automatic Daily Updates for New Releases
def schedule_daily_updates():
    while True:
        now = datetime.now()
        target_time = now.replace(hour=9, minute=0, second=0, microsecond=0)  # Daily at 9 AM
        if now > target_time:
            target_time += timedelta(days=1)

        time.sleep((target_time - now).total_seconds())

        # Fetch daily new releases
        url = f"https://www.googleapis.com/customsearch/v1?q=new+movie+releases+today&key={GOOGLE_API_KEY}&cx={CX}"
        response = requests.get(url).json()

        if 'items' in response:
            message = "🎬 *Today's New Releases:*\n"
            for item in response['items'][:5]:  # Top 5 releases
                title = item.get('title')
                snippet = item.get('snippet')
                message += f"\n• *{title}*\n📝 {snippet}\n"

            bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')

# ✅ Main Function
def main():
    global bot
    bot = Bot(token=BOT_TOKEN)
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("movie_details", movie_details))
    dp.add_handler(CommandHandler("watch", watch))
    dp.add_handler(CallbackQueryHandler(button_handler))

    # Start daily update scheduler
    threading.Thread(target=schedule_daily_updates, daemon=True).start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
