from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from services.lyrics_provider import search_lyric

router = APIRouter()

@router.get("/lyrics")
async def get_lyrics(
    keyword: str = Query(..., description="Song name and artist"),
    format: str = Query("text", description="Response format: 'text' or 'json'")
):
    """
    Get lyrics for a song.
    """
    lrc_content = await search_lyric(keyword)
    
    if not lrc_content:
        return JSONResponse(status_code=404, content={"error": "Lyrics not found"})

    if format == "json":
        return {"code": 200, "lyrics": lrc_content}
    else:
        return PlainTextResponse(content=lrc_content)
