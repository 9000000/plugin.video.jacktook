from dataclasses import dataclass, field
from typing import List

@dataclass
class TorrentStream:
    """
    Represents a single torrent stream. This data structure is used across the addon
    to standardize the information from different torrent providers.
    """
    title: str = ""
    type: str = ""
    debridType: str = ""
    indexer: str = ""
    guid: str = ""
    infoHash: str = ""
    size: int = 0
    seeders: int = 0
    peers: int = 0
    languages: List[str] = field(default_factory=list)
    fullLanguages: str = ""
    provider: str = ""
    publishDate: str = ""
    quality: str = "N/A"
    url: str = ""
    isPack: bool = False
    isCached: bool = False