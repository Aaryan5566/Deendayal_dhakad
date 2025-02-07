import requests
from pyrogram import Client, filters

# API KEYS
TMDB_API_KEY = "2937f761448c84e103d3ea8699d5a33c"
OMDB_API_KEY = "223e6df"  # Yahan apni OMDB API key daalo

# **Har Country Ki Movies Fetch Karne Ke Liye Languages Aur Regions**
LANGUAGES = ["en", "hi", "ta", "te", "ml", "kn", "bn", "ur", "pa", "fr", "es", "zh", "ja", "ru", "de", "ko", "ar", "it"]
REGIONS = ["IN", "US", "FR", "JP", "CN", "KR", "DE", "ES", "RU", "AE", "BR"]

def get_latest_movies():
    movie_list = []
    
    for lang in LANGUAGES:  
        for region in REGIONS:  
            url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={TMDB_API_KEY}&language={lang}&region={region}&page=1"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                movies = data.get("results", [])

                for movie in movies:
                    title = movie.get("title", "Unknown")
                    poster_path = movie.get("poster_path")
                    imdb_id = get_imdb_id(movie.get("id"))
                    overview = movie.get("overview", "No description available.")
                    release_date = movie.get("release_date", "Unknown Date")
                    language = movie.get("original_language", "Unknown").upper()
                    imdb_rating = get_imdb_rating(imdb_id)

                    full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

                    movie_list.append({
                        "title": title,
                        "poster_url": full_poster_url,
                        "imdb_id": imdb_id,
                        "imdb_rating": imdb_rating,
                        "overview": overview,
                        "release_date": release_date,
                        "language": language
                    })

            else:
                continue  

    return movie_list[:10]  

# ✅ IMDB ID Fetch Karne Ka Function
def get_imdb_id(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("imdb_id", "N/A")
    return "N/A"

# ✅ IMDB Rating Fetch Karne Ka Function
def get_imdb_rating(imdb_id):
    if imdb_id == "N/A":
        return "Not Available"
    
    url = f"https://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("imdbRating", "N/A")
    return "N/A"

# ✅ /movies Command Ko Handle Karna
@Client.on_message(filters.command("movies"))
async def movies_command(client, message):
    movies = get_latest_movies()

    if not movies:
        await message.reply_text("🎬 No new movies found.")
        return

    for movie in movies:
        caption = f"🎬 **{movie['title']}**\n"
        caption += f"🌍 Language: {movie['language']}\n"
        caption += f"📅 Release Date: {movie['release_date']}\n"
        caption += f"⭐ IMDB Rating: {movie['imdb_rating']}\n"
        caption += f"🎭 [IMDB Link](https://www.imdb.com/title/{movie['imdb_id']})\n"
        caption += f"📖 Story: {movie['overview']}"

        if movie["poster_url"]:
            await client.send_photo(message.chat.id, movie["poster_url"], caption=caption)
        else:
            await message.reply_text(caption)
