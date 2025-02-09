import os
import random
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ TMDb API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ Custom Image URL (इसे आप बदल सकते हैं)
CUSTOM_IMAGE_URL = "https://envs.sh/aWP.jpg"

# ✅ Random Reactions (🤡🫡🥰😇)
REACTIONS = ["🤡", "🫡", "🥰", "😇"]

# ✅ TMDb API से मूवी डेटा लाने का फ़ंक्शन
def get_movies(category):
    url_dict = {
        "trending": f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}&sort_by=vote_average.desc",
        "mustwatch": f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}",
        "hollywood": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_original_language=en&sort_by=vote_average.desc",
        "bollywood": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_original_language=hi&sort_by=vote_average.desc",
        "scifi": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=878&sort_by=vote_average.desc",
        "series": f"https://api.themoviedb.org/3/trending/tv/week?api_key={TMDB_API_KEY}",
        "comedy": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=35&sort_by=vote_average.desc",
        "horror": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=27&sort_by=vote_average.desc",
        "marvel": f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query=Marvel&sort_by=vote_average.desc",
        "dc": f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query=DC&sort_by=vote_average.desc",
        "anime": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=16&sort_by=vote_average.desc"
    }

    response = requests.get(url_dict[category])
    if response.status_code == 200:
        return response.json().get("results", [])[:40]  # सिर्फ़ 40 मूवीज़ दिखेंगी
    return []

# ✅ "/watch" कमांड हैंडलर
@Client.on_message(filters.command("watch"))
async def watch_command(client, message):
    user_name = message.from_user.first_name
    reaction = random.choice(REACTIONS)  # 🔥 Random Reaction

    buttons = [
        [InlineKeyboardButton("🔥 Trending", callback_data="trending"), InlineKeyboardButton("🌟 Must Watch", callback_data="mustwatch")],
        [InlineKeyboardButton("🎬 Hollywood", callback_data="hollywood"), InlineKeyboardButton("🇮🇳 Bollywood", callback_data="bollywood")],
        [InlineKeyboardButton("🚀 Sci-Fi", callback_data="scifi"), InlineKeyboardButton("📺 Series", callback_data="series")],
        [InlineKeyboardButton("😂 Comedy", callback_data="comedy"), InlineKeyboardButton("👻 Horror", callback_data="horror")],
        [InlineKeyboardButton("🦸‍♂️ Marvel", callback_data="marvel"), InlineKeyboardButton("🦇 DC Movies", callback_data="dc")],
        [InlineKeyboardButton("🎌 Anime", callback_data="anime")],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ]
    
    # ✅ Reaction + Image + Category Buttons
    await message.react(reaction)
    await message.reply_photo(
        photo=CUSTOM_IMAGE_URL,
        caption=f"👋 **Hey {user_name}**\n\n🎥 Cʜᴏᴏsᴇ Pʀᴇғᴇʀʀᴇᴅ Cᴀᴛᴇɢᴏʀʏ:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ Callback Query Handler (मूवी लिस्ट दिखाने के लिए)
@Client.on_callback_query()
async def callback_handler(client, query):
    category = query.data

    # 🔴 अगर "Close" बटन दबाया गया तो मैसेज हटाएँ
    if category == "close":
        await query.message.delete()
        return

    movies = get_movies(category)
    if not movies:
        await query.answer("❌ No movies found!", show_alert=True)
        return

    # Pagination सेटअप (हर पेज में 10 मूवीज़)
    page = 0
    await show_movies(client, query.message, category, page, movies)

# ✅ Show Movies with Pagination
async def show_movies(client, message, category, page, movies):
    total_pages = len(movies) // 10
    start_index = page * 10
    end_index = start_index + 10
    movies_list = movies[start_index:end_index]

    buttons = []
    for movie in movies_list:
        title = movie.get("title", "Unknown")
        buttons.append([InlineKeyboardButton(f"🎬 {title}", switch_inline_query_current_chat=title)])

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data=f"{category}_prev_{page-1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"{category}_next_{page+1}"))

    buttons.append(nav_buttons) if nav_buttons else None
    buttons.append([InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")])

    await message.edit_text(
        text=f"🎬 **Top {category.capitalize()} Movies (Page {page+1}):**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ✅ Pagination Handlers
@Client.on_callback_query(filters.regex(r"^(.*)_(prev|next)_(\d+)$"))
async def pagination_handler(client, query):
    category, action, page = query.data.rsplit("_", 2)
    page = int(page)
    movies = get_movies(category)
    await show_movies(client, query.message, category, page, movies)

# ✅ Main Menu वापस जाने का Handler
@Client.on_callback_query(filters.regex("main_menu"))
async def main_menu_handler(client, query):
    await watch_command(client, query.message)
