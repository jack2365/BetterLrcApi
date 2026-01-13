from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from services.lyrics_provider import search_lyric

router = APIRouter()

@router.get("/lyrics")
@router.post("/lyrics")
async def get_lyrics(
    keyword: str = Query(None, description="Song name and artist"),
    title: str = Query(None, description="Song title"),
    artist: str = Query(None, description="Artist name"),
    format: str = Query("text", description="Response format: 'text' or 'json'")
):
    """
    Get lyrics for a song. Supports 'keyword' OR 'title'+'artist'.
    """
    # Construct search keyword if not provided directly
    if not keyword:
        parts = []
        if artist: parts.append(artist)
        if title: parts.append(title)
        if parts:
            keyword = " ".join(parts)
        else:
             return JSONResponse(status_code=400, content={"error": "Missing parameters. Provide 'keyword' or 'title'/'artist'."})


    lrc_content = await search_lyric(keyword)
    
    if not lrc_content:
        return JSONResponse(status_code=404, content={"error": "Lyrics not found"})

    if format == "json":
        return {"code": 200, "lyrics": lrc_content}
    else:
        return PlainTextResponse(content=lrc_content)
