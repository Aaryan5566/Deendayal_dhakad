import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

# ✅ Random Reactions (🤡🫡🥰😇)
REACTIONS = ["🤡", "🫡", "🥰", "😇"]

# ✅ Categories with IMDb URLs
CATEGORIES = {
    "trending": ("🔥 Trending", "https://www.imdb.com/chart/moviemeter/"),
    "mustwatch": ("🌟 Must Watch", "https://www.imdb.com/chart/top/"),
    "hollywood": ("🎬 Hollywood", "https://www.imdb.com/search/title/?title_type=feature&languages=en"),
    "bollywood": ("🇮🇳 Bollywood", "https://www.imdb.com/search/title/?title_type=feature&languages=hi"),
    "scifi": ("🚀 Sci-Fi", "https://www.imdb.com/search/title/?genres=sci-fi"),
    "series": ("📺 Series", "https://www.imdb.com/chart/toptv/"),
    "comedy": ("😂 Comedy", "https://www.imdb.com/search/title/?genres=comedy"),
    "horror": ("👻 Horror", "https://www.imdb.com/search/title/?genres=horror"),
    "marvel": ("🦸‍♂️ Marvel", "https://www.imdb.com/search/title/?keywords=marvel-cinematic-universe"),
    "anime": ("🎌 Anime", "https://www.imdb.com/search/title/?genres=animation"),
    "dc": ("🦇 DC Movies", "https://www.imdb.com/search/title/?keywords=dc-comics"),
    "adult": ("🔞 Adult", "https://www.imdb.com/search/title/?genres=adult"),
}

# ✅ IMDb Scraping Function
def get_imdb_movies(category):
    category_name, url = CATEGORIES.get(category, ("Unknown", ""))
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = []
    movie_items = soup.find_all("td", class_="titleColumn")[:100]  # 100 Movies Scrape करें
    ratings = soup.find_all("td", class_="ratingColumn imdbRating")

    for i in range(len(movie_items)):
        title = movie_items[i].a.text.strip()
        link = "https://www.imdb.com" + movie_items[i].a["href"]
        rating = ratings[i].strong.text.strip() if ratings[i].strong else "N/A"

        movies.append({"title": title, "rating": rating, "link": link})

    return movies

# ✅ "/watch" Command Handler
@Client.on_message(filters.command("watch"))
async def watch_command(client, message):
    user_name = message.from_user.first_name
    reaction = random.choice(REACTIONS)

    buttons = [[InlineKeyboardButton(emoji, callback_data=key)] for key, (emoji, _) in CATEGORIES.items()]
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
        rating = movie["rating"]
        link = movie["link"]
        buttons.append([InlineKeyboardButton(f"⭐ {rating} | {title}", url=link)])

    # Pagination बटन सेटअप
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"{category}_prev_{page-1}"))
    nav_buttons.append(InlineKeyboardButton(f"🏠 {page+1}/{total_pages}", callback_data="main_menu"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"{category}_next_{page+1}"))

    buttons.append(nav_buttons) if nav_buttons else None
    await message.edit_text(
        text=f"🎬 **Top {CATEGORIES[category][0]} Movies (Page {page+1}):**",
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
