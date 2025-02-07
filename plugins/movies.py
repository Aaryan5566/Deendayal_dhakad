import requests
from pyrogram import Client, filters
import time

# TMDb API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# TMDb se movies fetch karne ka function
def get_latest_movies():
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])
        if not movies:
            return "No new movies found."

        movie_list = []
        for movie in movies[:10]:  # Sirf 10 movies fetch karega
            title = movie.get("title", "Unknown")
            release_date = movie.get("release_date", "Unknown")
            poster_path = movie.get("poster_path")
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            movie_id = movie.get("id")

            # IMDB aur description ke liye API call
            imdb_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
            imdb_response = requests.get(imdb_url)
            imdb_data = imdb_response.json() if imdb_response.status_code == 200 else {}
            imdb_rating = imdb_data.get("vote_average", "N/A")
            overview = imdb_data.get("overview", "No description available.")

            movie_list.append({
                "title": title,
                "release_date": release_date,
                "poster_url": full_poster_url,
                "imdb_rating": imdb_rating,
                "overview": overview
            })

        return movie_list
    else:
        return "Error fetching movies."

# /movies command ke liye
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    movies = get_latest_movies()

    if isinstance(movies, str):
        await message.reply_text(f"🎬 **Latest Movies:**\n\n{movies}")
        return

    for movie in movies:
        caption = f"**🎬 {movie['title']}**\n📅 Release Date: {movie['release_date']}\n⭐ IMDB: {movie['imdb_rating']}\n📖 {movie['overview']}"
        if movie["poster_url"]:
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:
            await message.reply_text(caption)
