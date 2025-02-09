import os
import requests
from telethon import events, Button

# TMDb API Key (अपनी API Key डालें)
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# TMDb API से मूवी डेटा लाने का फ़ंक्शन
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
        return response.json().get("results", [])[:5]  # सिर्फ 5 मूवीज़ दिखेंगी
    return []

# "/watch" कमांड हैंडलर
@bot.on(events.NewMessage(pattern="/watch"))
async def watch_command(event):
    buttons = [
        [Button.inline("🔥 Trending", b"trending"), Button.inline("🌟 Must Watch", b"mustwatch")],
        [Button.inline("🎬 Hollywood", b"hollywood"), Button.inline("🇮🇳 Bollywood", b"bollywood")],
        [Button.inline("🚀 Sci-Fi", b"scifi"), Button.inline("📺 Series", b"series")],
        [Button.inline("😂 Comedy", b"comedy"), Button.inline("👻 Horror", b"horror")],
        [Button.inline("🦸‍♂️ Marvel", b"marvel"), Button.inline("🎌 Anime", b"anime")],
        [Button.inline("❌ Close", b"close")]
    ]
    await event.reply("🎥 **Choose a category:**", buttons=buttons)

# Callback हैंडलर
@bot.on(events.CallbackQuery)
async def callback_handler(event):
    category = event.data.decode("utf-8")

    # Close button दबाने पर मैसेज हटाएं
    if category == "close":
        await event.edit("❌ Menu Closed.", buttons=None)
        return

    movies = get_movies(category)
    if not movies:
        await event.answer("No movies found!", alert=True)
        return

    buttons = []
    for movie in movies:
        title = movie.get("title", "Unknown")
        search_query = title.replace(" ", "+")
        buttons.append([Button.inline(f"🔍 {title}", data=f"search_{search_query}")])

    buttons.append([Button.inline("⬅️ Back", b"back")])
    await event.edit(f"🎬 **Top {category.capitalize()} Movies:**", buttons=buttons)

# Search बटन के लिए Callback
@bot.on(events.CallbackQuery(pattern=b"search_"))
async def search_handler(event):
    query = event.data.decode("utf-8").replace("search_", "").replace("+", " ")
    await event.respond(f"🔎 Searching for **{query}**...\n\n👉 [Click here](https://t.me/{bot.username}?q={query}) to search directly in Telegram.")
