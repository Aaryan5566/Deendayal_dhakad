import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

# ✅ Random Reactions (🤡🫡🥰😇)
REACTIONS = ["🤡", "🫡", "🥰", "😇"]

# ✅ Categories with Emojis
CATEGORIES = {
    "trending": "🔥 Trending",
    "mustwatch": "🌟 Must Watch",
    "hollywood": "🎬 Hollywood",
    "bollywood": "🇮🇳 Bollywood",
    "scifi": "🚀 Sci-Fi",
    "series": "📺 Series",
    "comedy": "😂 Comedy",
    "horror": "👻 Horror",
    "marvel": "🦸‍♂️ Marvel",
    "anime": "🎌 Anime",
    "dc": "🦇 DC Movies"
}

# ✅ Google से IMDb Rating Scrape करने का फ़ंक्शन
def get_imdb_rating(title):
    search_url = f"https://www.google.com/search?q={title}+IMDb+rating"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    rating = "N/A"
    for span in soup.find_all("span"):
        text = span.text.strip()
        if "/10" in text:
            rating = text
            break

    return rating

# ✅ Google से Movies Scrape करने का फ़ंक्शन
def get_movies(category):
    search_query = category.replace(" ", "+") + "+movies"
    search_url = f"https://www.google.com/search?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = []
    for result in soup.select("h3")[:100]:  # टॉप 100 मूवीज़ लें
        title = result.text.strip()
        rating = get_imdb_rating(title)
        movies.append({"title": title, "rating": rating})

    return movies

# ✅ IMDb Rating के हिसाब से Emoji सेट करने का फ़ंक्शन
def get_rating_emoji(rating):
    try:
        rating = float(rating.split("/")[0])
    except:
        return "🎬"

    if rating >= 8:
        return "🔥"
    elif rating >= 7:
        return "⭐"
    elif rating >= 6:
        return "👍"
    else:
        return "🎬"

# ✅ "/watch" कमांड हैंडलर
@Client.on_message(filters.command("watch"))
async def watch_command(client, message):
    user_name = message.from_user.first_name
    reaction = random.choice(REACTIONS)  # 🔥 Random Reaction

    buttons = [[InlineKeyboardButton(emoji, callback_data=key)] for key, emoji in CATEGORIES.items()]
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close")])
    
    # ✅ Reaction + Category Buttons
    await message.react(reaction)
    await message.reply_text(
        f"👋 **Hey {user_name}**\n\n🎥 Cʜᴏᴏsᴇ Pʀᴇғᴇʀʀᴇᴅ Cᴀᴛᴇɢᴏʀʏ:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ Callback Query Handler
@Client.on_callback_query()
async def callback_handler(client, query):
    category = query.data

    if category == "close":
        await query.message.delete()
        return

    movies = get_movies(category)
    page = 0
    await show_movies(client, query.message, category, page, movies)

# ✅ Show Movies with Pagination + IMDb Rating + Emoji
async def show_movies(client, message, category, page, movies):
    total_pages = (len(movies) - 1) // 10 + 1  
    start_index = page * 10
    end_index = start_index + 10
    movies_list = movies[start_index:end_index]

    buttons = []
    for movie in movies_list:
        title = movie["title"]
        imdb_rating = movie["rating"]
        emoji = get_rating_emoji(imdb_rating)
        buttons.append([InlineKeyboardButton(f"{emoji} {imdb_rating} | {title}", switch_inline_query_current_chat=title)])

    # Pagination बटन सेटअप
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"{category}_prev_{page-1}"))
    nav_buttons.append(InlineKeyboardButton(f"🏠 {page+1}/{total_pages}", callback_data="main_menu"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"{category}_next_{page+1}"))

    buttons.append(nav_buttons) if nav_buttons else None
    await message.edit_text(
        text=f"🎬 **Top {CATEGORIES[category]} (Page {page+1}):**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ Pagination Handlers
@Client.on_callback_query(filters.regex(r"^(.*)_(prev|next)_(\d+)$"))
async def pagination_handler(client, query):
    category, action, page = query.data.rsplit("_", 2)
    page = int(page)
    movies = get_movies(category)
    await show_movies(client, query.message, category, page, movies)

# ✅ Main Menu Handler
@Client.on_callback_query(filters.regex("main_menu"))
async def main_menu_handler(client, query):
    await watch_command(client, query.message)
