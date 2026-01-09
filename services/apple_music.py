import aiohttp
import urllib.parse
from active_cache import async_cache

@async_cache
async def search_apple_cover(keyword: str):
    """
    Search for a song cover on Apple Music (iTunes Search API).
    Returns the high-resolution artwork URL (1000x1000) or None.
    """
    if not keyword:
        return None
        
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://itunes.apple.com/search?term={encoded_keyword}&entity=song&limit=1&country=CN"
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Apple Music API Error: {response.status}")
                    return None
                
                data = await response.json(content_type=None)
                print(f"Apple Music Search Result: {data.get('resultCount')} items found.")
                
                if data.get("resultCount", 0) > 0:
                    result = data["results"][0]
                    artwork = result.get("artworkUrl100")
                    if artwork:
                        # Upgrade to high resolution (1000x1000)
                        # Example: .../100x100bb.jpg -> .../1000x1000bb.jpg
                        high_res_artwork = artwork.replace("100x100bb", "1000x1000bb")
                        return high_res_artwork
        except Exception as e:
            print(f"Error fetching from Apple Music: {e}")
            return None
    return None
