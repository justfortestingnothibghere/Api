from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Use Jinja2 for optional HTML template rendering
templates = Jinja2Templates(directory="templates")

# Your Supabase-hosted songs database
songs_db = [
    {
        "id": 1,
        "title": "Heat Waves",
        "artist": "Glass Animals",
        "song_url": "https://buenbdkodjrpzsfjsddu.supabase.co/storage/v1/object/public/profiles/Fireplace%20-%20Emin%20feat%20Jony%20tiktok%20remix%20%20%20best%20part%20%20%20slowed%20%20reverb.mp3",
        "thumbnail_url": "https://buenbdkodjrpzsfjsddu.supabase.co/storage/v1/object/public/profiles/bg.png"
    },
    {
        "id": 2,
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "song_url": "https://buenbdkodjrpzsfjsddu.supabase.co/storage/v1/object/public/profiles/music1.mp3",
        "thumbnail_url": "https://buenbdkodjrpzsfjsddu.supabase.co/storage/v1/object/public/profiles/bg.png"
    }
]

# Valid API keys
API_KEYS = {
    "Mr.arman.api.v1.songs.api": "access_single",
    "api.key.mrarman.all.1122": "access_all"
}

@app.middleware("http")
async def check_api_key(request: Request, call_next):
    """Middleware to check API keys for /api/v1 routes"""
    if request.url.path.startswith("/api/v1"):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key not in API_KEYS:
            raise HTTPException(status_code=403, detail="Invalid API key")
    return await call_next(request)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Simple welcome page"""
    html = """
    <html>
        <head><title>Music API</title></head>
        <body style="font-family:sans-serif;text-align:center;padding:40px;">
            <h1>🎵 Music API is Live!</h1>
            <p>Use the following endpoints:</p>
            <ul style="list-style:none;">
                <li><b>/api/v1/all/songs/</b> — get all songs (API key: api.key.mrarman.all.1122)</li>
                <li><b>/api/v1/access/songs/?title=Heat%20Waves</b> — get single song (API key: Mr.arman.api.v1.songs.api)</li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.get("/api/v1/all/songs/")
def get_all_songs(request: Request):
    """Return all songs in the database"""
    api_key = request.headers.get("x-api-key")
    if API_KEYS.get(api_key) != "access_all":
        raise HTTPException(status_code=403, detail="Unauthorized API key")
    return {"total_songs": len(songs_db), "songs": songs_db}

@app.get("/api/v1/access/songs/")
def get_song(title: str, request: Request):
    """Return a single song by title"""
    api_key = request.headers.get("x-api-key")
    if API_KEYS.get(api_key) != "access_single":
        raise HTTPException(status_code=403, detail="Unauthorized API key")

    for song in songs_db:
        if song["title"].lower() == title.lower():
            return {"status": "success", "song": song}
    raise HTTPException(status_code=404, detail="Song not found")
