from fastapi import APIRouter, Query, Response
from fastapi.responses import RedirectResponse, JSONResponse
from services.apple_music import search_apple_cover

router = APIRouter()

@router.get("/cover")
async def get_cover(
    keyword: str = Query(None, description="Song name and artist"),
    title: str = Query(None, description="Song title"),
    artist: str = Query(None, description="Artist name"),
    format: str = Query("redirect", description="Response format: 'redirect' or 'json'")
):
    """
    Get high-quality cover art from Apple Music. Supports 'keyword' OR 'title'+'artist'.
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

    cover_url = await search_apple_cover(keyword)
    
    if not cover_url:
        # Return a default placeholder or 404
        return JSONResponse(status_code=404, content={"error": "Cover not found"})

    if format == "json":
        return {"code": 200, "cover": cover_url}
    else:
        # Default behavior: Redirect to the image
        return RedirectResponse(url=cover_url)
