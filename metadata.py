import os
import requests
from typing import Optional, Tuple

# Using the fallback API key from the original addon.
# In a production environment, this should be handled more securely.
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "b70756b7083d9ee60f849d82d94a0d80")
BASE_URL = "https://api.themoviedb.org/3"

def get_metadata(imdb_id: str, media_type: str) -> Optional[Tuple[str, str]]:
    """
    Fetches metadata for a given IMDB ID from the TMDB API.

    Args:
        imdb_id: The IMDB ID of the movie or series.
        media_type: The type of content ('movie' or 'series').

    Returns:
        A tuple containing the title and TMDB ID, or None if not found.
    """
    if not TMDB_API_KEY:
        print("Error: TMDB_API_KEY is not set.")
        return None

    find_url = f"{BASE_URL}/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id"

    try:
        response = requests.get(find_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        results_key = "movie_results" if media_type == "movie" else "tv_results"

        if data.get(results_key):
            result = data[results_key][0]
            title = result.get("title") if media_type == "movie" else result.get("name")
            tmdb_id = result.get("id")
            if title and tmdb_id:
                return title, str(tmdb_id)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata from TMDB: {e}")

    return None