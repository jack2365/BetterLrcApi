import aiohttp
import os
import logging
from active_cache import async_cache
from services.kugou import KugouProvider

logger = logging.getLogger(__name__)

# Simplified Netease Search API
NETEASE_SEARCH_URL = "http://music.163.com/api/search/get/web"
NETEASE_LYRIC_URL = "http://music.163.com/api/song/lyric"

async def _search_netease(session, keyword: str):
    try:
        # 1. Search for the song ID
        params = {
            's': keyword,
            'type': 1,
            'offset': 0,
            'total': 'true',
            'limit': 1
        }
        # Headers to mimic a browser/client to avoid some blocks
        cookie = os.getenv("NETEASE_COOKIE", "")
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
            'origin': 'https://music.163.com',
            'referer': 'https://music.163.com',
            'cookie': cookie
        }
        
        async with session.post(NETEASE_SEARCH_URL, data=params, headers=headers) as resp:
            if resp.status != 200:
                return None
            data = await resp.json(content_type=None)
            
            if not isinstance(data, dict):
                return None

            songs = data.get('result', {}).get('songs', [])
            if not songs:
                return None
            
            song_id = songs[0]['id']
            
        # 2. Fetch lyric using song ID
        lyric_params = {
            'os': 'pc',
            'id': song_id,
            'lv': -1,
            'kv': -1,
            'tv': -1
        }
        async with session.get(NETEASE_LYRIC_URL, params=lyric_params, headers=headers) as lyric_resp:
            if lyric_resp.status != 200:
                return None
            lyric_data = await lyric_resp.json(content_type=None)
            
            lrc = lyric_data.get('lrc', {}).get('lyric')
            return lrc
            
    except Exception as e:
        logger.error(f"Netease Error: {e}")
        return None

@async_cache
async def search_lyric(keyword: str):
    """
    Aggragator: Netease -> Kugou
    """
    if not keyword:
        return None

    # Netease First
    async with aiohttp.ClientSession() as session:
        lrc = await _search_netease(session, keyword)
        if lrc:
            return lrc
    
    # Kugou Fallback
    print(f"Netease failed, trying Kugou for: {keyword}")
    try:
        lrc = await KugouProvider.get_lyrics(keyword)
        print(f"Kugou Result: {lrc[:50] if lrc else 'None'}")
        if lrc:
            return lrc
    except Exception as e:
        print(f"Kugou Provider Error: {e}")

    return "[00:00.00] No lyric found"
