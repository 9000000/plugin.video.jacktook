# Jacktook for Stremio

This is a Stremio addon converted from the original Jacktook Kodi addon. It uses Jackett to find and provide torrent streams for movies and TV shows directly within the Stremio application.

## Features

- **Jackett Integration**: Searches your configured Jackett instance for torrents.
- **TMDB Metadata**: Provides rich catalogs with posters and metadata from The Movie Database.
- **Movie and TV Show Support**: Works for both movies and series.

## Requirements

- Python 3.7+
- A running instance of [Jackett](https://github.com/Jackett/Jackett)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Copy the example configuration file:**
    ```bash
    cp config.ini.example config.ini
    ```
    *Note: A `config.ini` with placeholder values is already provided. You can edit it directly.*

2.  **Edit `config.ini` with your Jackett details:**
    Open the `config.ini` file and replace the placeholder values with your Jackett host URL and API key.

    ```ini
    [jackett]
    host = http://your-jackett-host:9117
    apikey = your-jackett-api-key
    ```

## Running the Addon

To start the addon server, run the following command in your terminal:

```bash
python3 addon.py
```

The addon will be running at `http://127.0.0.1:5000`.

## Adding to Stremio

1.  Open the Stremio application.
2.  Go to the Addons page.
3.  In the search bar at the top, paste the URL of your running addon: `http://127.0.0.1:5000/manifest.json`
4.  Press Enter.
5.  Click the "Install" button next to the Jacktook addon that appears.

You can now browse the "Jacktook Movies" catalog or click on any movie to find streams from your Jackett instance.