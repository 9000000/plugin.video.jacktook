import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional

# Re-use the same TMDB API key logic as in metadata.py
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "b70756b7083d9ee60f849d82d94a0d80")
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def _get_movie_details(movie_id: int) -> Optional[Dict]:
    """Fetches full details for a single movie, including its IMDB ID."""
    if not TMDB_API_KEY:
        return None

    url = f"{BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=external_ids"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def get_catalog(catalog_type: str, catalog_id: str) -> List[Dict]:
    """
    Fetches and formats a catalog of content from TMDB.
    """
    if catalog_type == "movie" and catalog_id == "jacktook-movies":
        # For now, we only support the "Popular Movies" catalog.
        popular_movies_url = f"{BASE_URL}/movie/popular?api_key={TMDB_API_KEY}"

        try:
            response = requests.get(popular_movies_url)
            response.raise_for_status()
            popular_movies = response.json().get("results", [])

            metas = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                # Fetch full details for each movie in parallel
                future_to_movie = {executor.submit(_get_movie_details, movie['id']): movie for movie in popular_movies}
                for future in as_completed(future_to_movie):
                    details = future.result()
                    if details and details.get("imdb_id"):
                        meta = {
                            "id": details["imdb_id"],
                            "type": "movie",
                            "name": details["title"],
                            "poster": f"{IMAGE_BASE_URL}{details['poster_path']}" if details.get('poster_path') else None,
                            "description": details.get("overview"),
                            "releaseInfo": details.get("release_date"),
                        }
                        metas.append(meta)
            return metas

        except requests.exceptions.RequestException as e:
            print(f"Error fetching popular movies from TMDB: {e}")

    return []