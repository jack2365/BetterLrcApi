import aiohttp
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

class LrclibProvider:
    """
    Provider for lrclib.net (Open Lyrics Database) without Auth
    """
    SEARCH_API = "https://lrclib.net/api/search"

    @classmethod
    async def get_lyrics(cls, keyword: str) -> str:
        """
        Search and return lyrics from Lrclib
        """
        async with aiohttp.ClientSession() as session:
            # 1. Search for the song
            # Lrclib supports searching by 'q' parameter which matches track_name, artist_name, album_name
            params = {'q': keyword}
            try:
                # SSL verification disabled to avoid local cert issues
                async with session.get(cls.SEARCH_API, params=params, timeout=10, ssl=False) as resp:
                    if resp.status != 200:
                        logger.warning(f"[Lrclib] Search failed: {resp.status}")
                        return None
                    
                    data = await resp.json()
                    if not isinstance(data, list) or not data:
                        logger.debug(f"[Lrclib] No results for: {keyword}")
                        return None
                    
                    # 2. Pick the best match
                    # We prioritize synced lyrics where syncedLyrics is not null
                    best_match = None
                    for track in data:
                        if track.get('syncedLyrics'):
                            best_match = track
                            break
                    
                    # Fallback to plain lyrics if no synced lyrics found
                    if not best_match and data:
                        best_match = data[0]
                        
                    if best_match:
                        # Return syncedLyrics if available, else plainLyrics
                        lrc = best_match.get('syncedLyrics') or best_match.get('plainLyrics')
                        if lrc:
                            logger.info(f"[Lrclib] Found lyrics for: {keyword} (ID: {best_match.get('id')})")
                            return lrc

                    return None
            except Exception as e:
                logger.error(f"[Lrclib] Error: {e}")
                return None
