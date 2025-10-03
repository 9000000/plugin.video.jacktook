import configparser
from typing import List
from clients.jackett import Jackett
from metadata import get_metadata
from domain import TorrentStream

def get_streams(media_type: str, imdb_id: str):
    """
    This function is the core of the Stremio addon.
    It takes a media type and an IMDB ID, fetches metadata, and then searches for streams.
    """
    print(f"Searching for streams for {media_type} with id {imdb_id}")

    # 1. Fetch metadata (title) from TMDB
    metadata = get_metadata(imdb_id, media_type)
    if not metadata:
        print(f"Could not find metadata for {imdb_id}")
        return []

    title, tmdb_id = metadata
    print(f"Found title: {title} (TMDB ID: {tmdb_id})")

    # 2. Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 3. Initialize torrent clients
    streams = []
    if 'jackett' in config:
        jackett_host = config['jackett'].get('host')
        jackett_apikey = config['jackett'].get('apikey')
        if jackett_host and jackett_apikey:
            jackett_client = Jackett(host=jackett_host, apikey=jackett_apikey)
            jackett_streams = jackett_client.search(query=title, media_type=media_type, imdb_id=imdb_id)
            print(f"Found {len(jackett_streams)} streams from Jackett.")
            streams.extend(jackett_streams)
        else:
            print("Jackett configuration is incomplete.")

    # In the future, other clients would be initialized and searched here.

    return streams