import requests
from pyrogram import Client, filters

# TMDb API Key
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"

# TMDb se latest movies fetch karna
def get_latest_movies():
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])
        if not movies:
            return "No new movies found."

        movie_list = []
        for index, movie in enumerate(movies[:10], start=1):
            title = movie.get("title", "Unknown")
            poster_path = movie.get("poster_path")
            imdb_id = movie.get("id")  # Movie ka IMDB ID
            overview = movie.get("overview", "No description available.")  # Storyline
            release_date = movie.get("release_date", "Unknown Date")  # Release Date

            # TMDb Poster URL
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            movie_list.append({
                "index": index,
                "title": title,
                "poster_url": full_poster_url,
                "imdb_id": imdb_id,
                "overview": overview,
                "release_date": release_date
            })

        return movie_list
    else:
        return "Error fetching movies."

# /movies command ka handler
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    movies = get_latest_movies()

    if isinstance(movies, str):
        await message.reply_text(f"🎬 Latest Movies:\n\n{movies}")
        return

    for movie in movies:
        caption = f"🎬 **{movie['index']}. {movie['title']}**\n"
        caption += f"📅 Release Date: {movie['release_date']}\n"
        caption += f"🎭 [IMDB Link](https://www.themoviedb.org/movie/{movie['imdb_id']})\n"
        caption += f"📖 Story: {movie['overview']}"

        if movie["poster_url"]:
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:
            await message.reply_text(caption)
