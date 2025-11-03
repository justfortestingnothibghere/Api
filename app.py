from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory="templates")

# Fake database (replace Supabase URLs here)
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
    # Skip HTML frontend route
    if request.url.path.startswith("/api/v1"):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key not in API_KEYS:
            raise HTTPException(status_code=403, detail="Invalid API key")
    return await call_next(request)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Frontend test page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/v1/access/songs/")
def get_song(title: str, request: Request):
    """Fetch single song by title"""
    api_key = request.headers.get("x-api-key")
    if API_KEYS[api_key] != "access_single":
        raise HTTPException(status_code=403, detail="Unauthorized API key")

    for song in songs_db:
        if song["title"].lower() == title.lower():
            return {"status": "success", "song": song}
    raise HTTPException(status_code=404, detail="Song not found")


@app.get("/api/v1/all/songs/")
def get_all_songs(request: Request):
    """Fetch all songs"""
    api_key = request.headers.get("x-api-key")
    if API_KEYS[api_key] != "access_all":
        raise HTTPException(status_code=403, detail="Unauthorized API key")

    return {"total_songs": len(songs_db), "songs": songs_db}