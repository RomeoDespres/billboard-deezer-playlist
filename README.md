# Billboard Hot 100 Deezer playlist

This repository contains the Python code to generate and update a Deezer playlist from the [Billboard Hot 100 chart](https://www.billboard.com/charts/hot-100).

The one I maintain with this code can be found [here](https://www.deezer.com/playlist/3687256962).

## Installation and usage

### 1. Clone the repository

```bash
$ git clone https://github.com/RomeoDespres/billboard-deezer-playlist
$ cd billboard-deezer-playlist
```

### 2. Install dependencies

```bash
$ pip install --user billboard.py requests tqdm
```

### 3. Update your playlist

```bash
$ python update_billboard_playlist
```

On first use, a Deezer API access token and a playlist ID will be asked. The access token can be obtained [here](https://developers.deezer.com/api/oauth), and the playlist ID can be found in the playlist URL which looks like `https://www.deezer.com/en/playlist/PLAYLIST_ID`.

These credentials will be stored in *billboard\_deezer\_playlist/credentials.json* in plain text. Be careful with wat you do with this file.

