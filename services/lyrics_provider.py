import aiohttp
from active_cache import async_cache

# Simplified Netease Search API
NETEASE_SEARCH_URL = "http://music.163.com/api/search/get/web"
NETEASE_LYRIC_URL = "http://music.163.com/api/song/lyric"

@async_cache
async def search_lyric(keyword: str):
    """
    Search for lyrics using Netease Cloud Music API.
    Returns: lrc content (string) or None.
    """
    if not keyword:
        return None
        
    async with aiohttp.ClientSession() as session:
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
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
                'origin': 'https://music.163.com',
                'referer': 'https://music.163.com',
            }
            
            print(f"Searching lyrics for: {keyword}")
            async with session.post(NETEASE_SEARCH_URL, data=params, headers=headers) as resp:
                if resp.status != 200:
                    print(f"Netease Search HTTP Error: {resp.status}")
                    return None
                data = await resp.json(content_type=None)
                
                if not isinstance(data, dict):
                    print(f"Netease: Unexpected data type: {type(data)} - {data}")
                    return None

                songs = data.get('result', {}).get('songs', [])
                if not songs:
                    print("Netease: No songs found.")
                    return None
                
                song_id = songs[0]['id']
                print(f"Netease: Found song ID {song_id}")
                
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
                if not lrc:
                    return "[00:00.00] No lyric found"
                
                return lrc
                
        except Exception as e:
            print(f"Error fetching lyrics: {e}")
            return None
    return None
