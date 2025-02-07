import requests
from pyrogram import Client, filters

# TMDb API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# TMDb से नवीनतम मूवीज़ प्राप्त करने का फ़ंक्शन
def get_latest_movies():
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])
        if not movies:
            return "No new movies found."

        movie_list = []
        for index, movie in enumerate(movies[:10], start=1):  # केवल शीर्ष 10 मूवीज़ दिखाएगा
            title = movie.get("title", "Unknown")
            poster_path = movie.get("poster_path")
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            movie_list.append((index, title, full_poster_url))

        return movie_list
    else:
        return "Error fetching movies."

# /movies कमांड को हैंडल करने का फ़ंक्शन
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    movies = get_latest_movies()

    if isinstance(movies, str):  # यदि कोई त्रुटि या खाली प्रतिक्रिया आई
        await message.reply_text(f"🎬 Latest Movies:\n\n{movies}")
        return

    for index, title, poster_url in movies:
        caption = f"**{index}. {title}**"
        if poster_url:
            await client.send_photo(message.chat.id, poster_url, caption=caption)
        else:
            await message.reply_text(caption)
