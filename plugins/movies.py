import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

# ✅ IMDb Top 100 Movies Scraper
def get_imdb_movies():
    url = "https://www.imdb.com/chart/top/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = []
    for item in soup.select("tbody.lister-list tr")[:100]:  # सिर्फ 100 मूवीज़ लें
        title = item.select_one(".titleColumn a").text
        rating = item.select_one(".ratingColumn strong").text
        movies.append({"title": title, "rating": rating})

    return movies

# ✅ IMDb Top Series Scraper
def get_imdb_series():
    url = "https://www.imdb.com/chart/toptv/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    series = []
    for item in soup.select("tbody.lister-list tr")[:40]:  # टॉप 40 वेब सीरीज़
        title = item.select_one(".titleColumn a").text
        rating = item.select_one(".ratingColumn strong").text
        series.append({"title": title, "rating": rating})

    return series

# ✅ IMDb Rating के हिसाब से Emoji
def get_rating_emoji(rating):
    rating = float(rating)
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
    buttons = [
        [InlineKeyboardButton("🎬 Top Movies", callback_data="movies"),
         InlineKeyboardButton("📺 Top Series", callback_data="series")],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ]
    
    await message.reply_text(
        "🎥 **Choose a category:**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ Callback Query Handler
@Client.on_callback_query()
async def callback_handler(client, query):
    category = query.data

    if category == "close":
        await query.message.delete()
        return

    movies = get_imdb_movies() if category == "movies" else get_imdb_series()
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

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"{category}_prev_{page-1}"))
    nav_buttons.append(InlineKeyboardButton(f"🏠 {page+1}/{total_pages}", callback_data="main_menu"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"{category}_next_{page+1}"))

    buttons.append(nav_buttons) if nav_buttons else None
    await message.edit_text(
        text=f"🎬 **Top {category.capitalize()} (Page {page+1}):**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ Pagination Handlers
@Client.on_callback_query(filters.regex(r"^(.*)_(prev|next)_(\d+)$"))
async def pagination_handler(client, query):
    category, action, page = query.data.rsplit("_", 2)
    page = int(page)
    movies = get_imdb_movies() if category == "movies" else get_imdb_series()
    await show_movies(client, query.message, category, page, movies)

# ✅ Main Menu Handler
@Client.on_callback_query(filters.regex("main_menu"))
async def main_menu_handler(client, query):
    await watch_command(client, query.message)
