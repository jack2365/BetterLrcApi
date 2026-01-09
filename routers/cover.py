from fastapi import APIRouter, Query, Response
from fastapi.responses import RedirectResponse, JSONResponse
from services.apple_music import search_apple_cover

router = APIRouter()

@router.get("/cover")
async def get_cover(
    keyword: str = Query(..., description="Song name and artist"),
    format: str = Query("redirect", description="Response format: 'redirect' or 'json'")
):
    """
    Get high-quality cover art from Apple Music.
    """
    cover_url = await search_apple_cover(keyword)
    
    if not cover_url:
        # Return a default placeholder or 404
        return JSONResponse(status_code=404, content={"error": "Cover not found"})

    if format == "json":
        return {"code": 200, "cover": cover_url}
    else:
        # Default behavior: Redirect to the image
        return RedirectResponse(url=cover_url)
