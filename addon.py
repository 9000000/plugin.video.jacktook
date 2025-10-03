from flask import Flask, jsonify
from stream_handler import get_streams
from catalog_handler import get_catalog
from domain import TorrentStream

app = Flask(__name__)

# Stremio Addon Manifest
# This is a crucial endpoint that provides Stremio with the addon's metadata.
# It tells Stremio what the addon can do, what content it provides, and how to interact with it.
manifest = {
    "id": "org.community.jacktook",
    "version": "0.14.0",
    "name": "Jacktook",
    "description": "Kodi addon for torrent streaming, now on Stremio!",
    "resources": [
        "catalog",
        "stream"
    ],
    "types": ["movie", "series"],
    "catalogs": [
        {"type": "movie", "id": "jacktook-movies", "name": "Jacktook Movies"},
        {"type": "series", "id": "jacktook-series", "name": "Jacktook TV Shows"}
    ],
    "idPrefixes": ["tt"]
}

@app.route('/manifest.json')
def get_manifest():
    """
    Provides the addon's manifest to Stremio.
    This is the first endpoint Stremio calls to understand the addon.
    """
    return jsonify(manifest)

@app.route('/catalog/<type>/<id>.json')
def get_catalog_endpoint(type: str, id: str):
    """
    Provides a catalog of content to Stremio.
    This endpoint is called when a user browses the addon's catalogs.
    """
    metas = get_catalog(type, id)
    return jsonify({"metas": metas})


def to_stremio_streams(torrents: list[TorrentStream]):
    """
    Converts a list of TorrentStream objects into the format expected by Stremio.
    """
    streams = []
    for torrent in torrents:
        stream = {
            "title": torrent.title,
            "infoHash": torrent.infoHash,
            "fileIdx": None, # Assuming one file per torrent for now
        }
        streams.append(stream)
    return streams

@app.route('/stream/<type>/<id>.json')
def get_stream(type: str, id: str):
    """
    This is the core endpoint that provides stream information to Stremio.
    It takes a type (movie or series) and an ID (IMDB ID) and returns a list of streams.
    """
    streams = get_streams(type, id)
    stremio_streams = to_stremio_streams(streams)
    return jsonify({"streams": stremio_streams})


if __name__ == '__main__':
    # The addon runs as a web server.
    # Stremio will make HTTP requests to the endpoints defined here.
    app.run(host='0.0.0.0', port=5000)