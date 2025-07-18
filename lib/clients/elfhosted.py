import re
from typing import List, Dict, Any, Optional, Callable
from lib.clients.base import BaseClient, TorrentStream
from lib.utils.kodi.utils import convert_size_to_bytes, translation


class Elfhosted(BaseClient):
    def __init__(self, host: str, notification: Callable) -> None:
        super().__init__(host, notification)

    def search(
        self,
        imdb_id: str,
        mode: str,
        media_type: str,
        season: Optional[int],
        episode: Optional[int],
    ) -> Optional[List[TorrentStream]]:
        try:
            if mode == "tv" or media_type == "tv":
                url = f"{self.host}/stream/series/{imdb_id}:{season}:{episode}.json"
            elif mode == "movies" or media_type == "movies":
                url = f"{self.host}/stream/{mode}/{imdb_id}.json"
            res = self.session.get(url, timeout=10)
            if res.status_code != 200:
                return
            response = self.parse_response(res)
            return response
        except Exception as e:
            self.handle_exception(f"{translation(30231)}: {str(e)}")

    def parse_response(self, res: any) -> List[TorrentStream]:
        res = res.json()
        results = []
        for item in res["streams"]:
            parsed_item = self.parse_stream_title(item["title"])
            results.append(
                TorrentStream(
                    title=parsed_item["title"],
                    type="Torrent",
                    indexer="Elfhosted",
                    guid=item["infoHash"],
                    infoHash=item["infoHash"],
                    size=parsed_item["size"],
                    publishDate="",
                    seeders=0,
                    peers=0,
                    languages=[],
                    fullLanguages="",
                    provider="",
                )
            )
        return results

    def parse_stream_title(self, title: str) -> Dict[str, Any]:
        name = title.splitlines()[0]

        size_match = re.search(r"💾 (\d+(?:\.\d+)?\s*(GB|MB))", title, re.IGNORECASE)
        size = size_match.group(1) if size_match else ""
        size = convert_size_to_bytes(size)

        return {
            "title": name,
            "size": size,
        }
