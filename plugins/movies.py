import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

# ✅ Google API Key और Search Engine ID
GOOGLE_API_KEY = "AIzaSyCOU_1R97pHgzDr7JgOhuNgvleFA2Bf0Go"
SEARCH_ENGINE_ID = "e2478349016e44cc9"

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
    "dc": "🦇 DC Movies",
    "adult": "🔞 Adult"
}

# ✅ Google API से IMDb Trending Movies Scrape करने का फ़ंक्शन
def get_imdb_movies(category):
    search_query = f"top 10 {category} movies 2024 site:imdb.com"
    url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    data = response.json()

    movies = []
    for item in data.get("items", [])[:100]:  # 100 Movies तक लाएं
        title = item["title"].split("- IMDb")[0].strip()  # Extra Text हटाएं
        link = item["link"]
        movies.append({"title": title, "link": link})

    return movies

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

    movies = get_imdb_movies(category)
    page = 0
    await show_movies(client, query.message, category, page, movies)

# ✅ Show Movies with Pagination (10 Buttons Per Page)
async def show_movies(client, message, category, page, movies):
    total_pages = (len(movies) - 1) // 10 + 1  
    start_index = page * 10
    end_index = start_index + 10
    movies_list = movies[start_index:end_index]

    buttons = []
    for movie in movies_list:
        title = movie["title"]
        link = movie["link"]
        buttons.append([InlineKeyboardButton(f"🎬 {title}", url=link)])

    # Pagination बटन सेटअप
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"{category}_prev_{page-1}"))
    nav_buttons.append(InlineKeyboardButton(f"🏠 {page+1}/{total_pages}", callback_data="main_menu"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"{category}_next_{page+1}"))

    buttons.append(nav_buttons) if nav_buttons else None
    await message.edit_text(
        text=f"🎬 **Top {CATEGORIES[category]} Movies (Page {page+1}):**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ Pagination Handlers
@Client.on_callback_query(filters.regex(r"^(.*)_(prev|next)_(\d+)$"))
async def pagination_handler(client, query):
    category, action, page = query.data.rsplit("_", 2)
    page = int(page)
    movies = get_imdb_movies(category)
    await show_movies(client, query.message, category, page, movies)

# ✅ Main Menu Handler
@Client.on_callback_query(filters.regex("main_menu"))
async def main_menu_handler(client, query):
    await watch_command(client, query.message)
