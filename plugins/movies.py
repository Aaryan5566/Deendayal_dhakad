import json
import requests
from datetime import datetime, timedelta
from threading import Timer

# TMDb API key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# Random Emojis
EMOJIS = ['🤡', '🥰', '😇', '🫡']

def get_movie_details(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()

    if not data['results']:
        return None

    movie = data['results'][0]
    movie_id = movie['id']

    # Fetching movie details
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    details_response = requests.get(details_url)
    if details_response.status_code != 200:
        return None
    details = details_response.json()

    title = details.get('title', 'N/A')
    release_date = details.get('release_date', 'N/A')
    overview = details.get('overview', 'No story available.')
    rating = details.get('vote_average', 'N/A')
    poster_path = details.get('poster_path', '')

    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    return {
        'title': title,
        'release_date': release_date,
        'overview': overview,
        'rating': rating,
        'poster_url': poster_url
    }

def delete_message_after_delay(bot, chat_id, message_id, delay=1200):
    Timer(delay, lambda: bot.delete_message(chat_id, message_id)).start()

def movie_details_handler(bot, update):
    message = update.get('message', {})
    chat_id = message.get('chat', {}).get('id')
    text = message.get('text', '')

    if not text.startswith('/movie_details'):
        return

    query = text.replace('/movie_details', '').strip()
    if not query:
        bot.send_message(chat_id, "कृपया मूवी का नाम लिखें जैसे:\n`/movie_details Inception`", parse_mode="Markdown")
        return

    details = get_movie_details(query)
    if not details:
        bot.send_message(chat_id, "मूवी नहीं मिली। कृपया सही नाम दर्ज करें।")
        return

    emoji = f"**{EMOJIS[datetime.now().second % len(EMOJIS)]}**"

    caption = f"""{emoji}

**🎬 नाम:** {details['title']}
**📅 रिलीज डेट:** {details['release_date']}
**⭐ IMDb रेटिंग:** {details['rating']}
**📝 कहानी:** {details['overview']}
"""

    # Sending movie poster with caption
    if details['poster_url']:
        sent_msg = bot.send_photo(chat_id, photo=details['poster_url'], caption=caption, parse_mode="Markdown",
                                  reply_markup=json.dumps({
                                      "inline_keyboard": [[
                                          {"text": "🎥 Get Movie", "switch_inline_query_current_chat": details['title']}
                                      ]]
                                  }))
    else:
        sent_msg = bot.send_message(chat_id, caption, parse_mode="Markdown",
                                    reply_markup=json.dumps({
                                        "inline_keyboard": [[
                                            {"text": "🎥 Get Movie", "switch_inline_query_current_chat": details['title']}
                                        ]]
                                    }))

    # Auto-delete after 20 minutes (1200 seconds)
    delete_message_after_delay(bot, chat_id, sent_msg['message_id'])

# Plugin settings for bot
def main(bot, update):
    movie_details_handler(bot, update)
