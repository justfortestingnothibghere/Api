from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mock songs database
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

# Allow browser (Render) test access without header (for debugging only)
ALLOW_BROWSER_TEST = True


@app.middleware("http")
async def check_api_key(request: Request, call_next):
    """Middleware to validate API key for protected routes."""
    path = request.url.path
    api_key = request.headers.get("x-api-key")

    # Debug info (shows in Render logs)
    print(f"Incoming request: {path}, Header key: {api_key}")

    if path.startswith("/api/v1"):
        # Allow access if browser testing is enabled
        if ALLOW_BROWSER_TEST and not api_key:
            print("⚠️ Allowing temporary browser test access (no API key)")
            return await call_next(request)

        if not api_key or api_key not in API_KEYS:
            return JSONResponse(
                status_code=403,
                content={"error": "Invalid or missing API key", "path": path}
            )

    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Simple homepage"""
    html = """
    <html>
        <head>
            <title>🎵 Music API</title>
            <style>
                body { font-family: Arial; background:#111; color:#eee; text-align:center; padding:50px; }
                h1 { color: #00e6e6; }
                code { background:#222; padding:5px 10px; border-radius:6px; }
            </style>
        </head>
        <body>
            <h1>🎧 Music API is Live!</h1>
            <p>Use these endpoints:</p>
            <ul style="list-style:none; text-align:left; display:inline-block;">
                <li>📦 <b>/api/v1/all/songs/</b> — all songs<br><code>x-api-key: api.key.mrarman.all.1122</code></li>
                <li>🎵 <b>/api/v1/access/songs/?title=Heat%20Waves</b> — single song<br><code>x-api-key: Mr.arman.api.v1.songs.api</code></li>
            </ul>
            <p>🧠 Tip: Use curl or Postman to test headers</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/api/v1/all/songs/")
async def get_all_songs(request: Request):
    """Return all songs (requires full access key)."""
    api_key = request.headers.get("x-api-key")

    if not ALLOW_BROWSER_TEST:
        if API_KEYS.get(api_key) != "access_all":
            raise HTTPException(status_code=403, detail="Unauthorized API key")

    return {"total_songs": len(songs_db), "songs": songs_db}


@app.get("/api/v1/access/songs/")
async def get_song(title: str, request: Request):
    """Return a single song (requires single-access key)."""
    api_key = request.headers.get("x-api-key")

    if not ALLOW_BROWSER_TEST:
        if API_KEYS.get(api_key) != "access_single":
            raise HTTPException(status_code=403, detail="Unauthorized API key")

    for song in songs_db:
        if song["title"].lower() == title.lower():
            return {"status": "success", "song": song}

    raise HTTPException(status_code=404, detail="Song not found")
