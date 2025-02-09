import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ TMDb API Key (अपनी API Key डालें)
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# ✅ TMDb API से मूवी डेटा लाने का फ़ंक्शन
def get_movies(category):
    url_dict = {
        "trending": f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}&sort_by=vote_average.desc",
        "mustwatch": f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}",
        "hollywood": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_original_language=en",
        "bollywood": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_original_language=hi",
        "scifi": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=878",
        "series": f"https://api.themoviedb.org/3/trending/tv/week?api_key={TMDB_API_KEY}",
        "comedy": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=35&sort_by=vote_average.desc",
        "horror": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=27&sort_by=vote_average.desc",
        "marvel": f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query=Marvel",
        "anime": f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres=16&sort_by=vote_average.desc"
    }

    response = requests.get(url_dict[category])
    if response.status_code == 200:
        return response.json().get("results", [])[:10]  # सिर्फ़ 10 मूवीज़ दिखेंगी
    return []

# ✅ "/watch" कमांड हैंडलर
@Client.on_message(filters.command("watch"))
async def watch_command(client, message):
    buttons = [
        [InlineKeyboardButton("🔥 Trending", callback_data="trending"), InlineKeyboardButton("🌟 Must Watch", callback_data="mustwatch")],
        [InlineKeyboardButton("🎬 Hollywood", callback_data="hollywood"), InlineKeyboardButton("🇮🇳 Bollywood", callback_data="bollywood")],
        [InlineKeyboardButton("🚀 Sci-Fi", callback_data="scifi"), InlineKeyboardButton("📺 Series", callback_data="series")],
        [InlineKeyboardButton("😂 Comedy", callback_data="comedy"), InlineKeyboardButton("👻 Horror", callback_data="horror")],
        [InlineKeyboardButton("🦸‍♂️ Marvel", callback_data="marvel"), InlineKeyboardButton("🎌 Anime", callback_data="anime")],
        [InlineKeyboardButton("❌ Close", callback_data="close")]
    ]
    await message.reply_text("🎥 **Choose a category:**", reply_markup=InlineKeyboardMarkup(buttons))

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

    buttons = []
    for movie in movies:
        title = movie.get("title", "Unknown")
        search_query = title.replace(" ", "+")
        buttons.append([InlineKeyboardButton(f"🔍 {title}", switch_inline_query_current_chat=title)])

    buttons.append([InlineKeyboardButton("⬅️ Back", callback_data="back")])
    await query.message.edit_text(f"🎬 **Top {category.capitalize()} Movies:**", reply_markup=InlineKeyboardMarkup(buttons))
