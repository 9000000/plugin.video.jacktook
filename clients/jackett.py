import requests
import xmltodict
from typing import List, Optional
from domain import TorrentStream

class Jackett:
    def __init__(self, host: str, apikey: str, timeout: int = 10):
        self.host = host.rstrip("/")
        self.apikey = apikey
        self.timeout = timeout
        self.base_url = f"{self.host}/api/v2.0/indexers/all/results/torznab/api?apikey={self.apikey}"

    def _build_url(
        self,
        query: str,
        media_type: str,
        imdb_id: str,
        season: Optional[int] = None,
        episode: Optional[int] = None,
    ) -> str:
        url = f"{self.base_url}&q={query.replace(' ', '+')}"

        if media_type == "movie":
            url += f"&t=movie&imdbid={imdb_id}"
        elif media_type == "series":
            url += f"&t=tvsearch&imdbid={imdb_id.replace('tt', '')}"
            if season and episode:
                url += f"&season={season}&ep={episode}"

        return url

    def search(
        self,
        query: str,
        media_type: str,
        imdb_id: str,
        season: Optional[int] = None,
        episode: Optional[int] = None,
    ) -> List[TorrentStream]:
        try:
            url = self._build_url(query, media_type, imdb_id, season, episode)
            response = requests.get(url, timeout=self.timeout)
            if response.status_code != 200:
                print(f"Jackett API request failed with status code {response.status_code}")
                return []
            return self._parse_response(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Jackett: {e}")
            return []

    def _parse_response(self, content: bytes) -> List[TorrentStream]:
        try:
            res_dict = xmltodict.parse(content)
            channel = res_dict.get("rss", {}).get("channel", {})
            items = channel.get("item", [])
            if not items:
                return []

            results = []
            # Ensure items is a list
            if not isinstance(items, list):
                items = [items]

            for item in items:
                stream = self._extract_stream(item)
                if stream:
                    results.append(stream)
            return results
        except Exception as e:
            print(f"Error parsing Jackett XML response: {e}")
            return []

    def _extract_stream(self, item: dict) -> Optional[TorrentStream]:
        attrs = item.get("torznab:attr", [])
        if isinstance(attrs, dict): # handle case where there is only one attribute
            attrs = [attrs]

        attributes = {attr.get("@name"): attr.get("@value") for attr in attrs}
        info_hash = attributes.get("infohash")

        if not info_hash:
            return None # Skip torrents without an infohash

        return TorrentStream(
            title=item.get("title", "N/A"),
            type="torrent",
            indexer="Jackett",
            provider=item.get("jackettindexer", {}).get("#text", "Unknown"),
            guid=item.get("guid"),
            infoHash=info_hash.upper(),
            size=int(item.get("size", 0)),
            seeders=int(attributes.get("seeders", 0)),
            peers=int(attributes.get("peers", 0)),
            languages=[],
            quality=item.get("quality", "N/A"),
        )