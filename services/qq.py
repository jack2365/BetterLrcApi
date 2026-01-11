import aiohttp
import base64
import html
import logging

logger = logging.getLogger(__name__)

class QQProvider:
    SEARCH_API = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    LYRIC_API = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"

    @classmethod
    async def get_lyrics(cls, keyword: str) -> str:
        async with aiohttp.ClientSession() as session:
            # 1. Search Song
            song_info = await cls._search_song(session, keyword)
            if not song_info:
                logger.debug(f"[QQ] No song found for {keyword}")
                return None
            
            song_mid = song_info.get('songmid')
            if not song_mid:
                return None
                
            # 2. Get Lyrics
            return await cls._get_lyric_by_mid(session, song_mid)

    @classmethod
    async def _search_song(cls, session, keyword):
        params = {
            'w': keyword,
            'p': 1,
            'n': 1,
            'format': 'json'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://y.qq.com/'
        }
        try:
            async with session.get(cls.SEARCH_API, params=params, headers=headers) as resp:
                data = await resp.json(content_type=None)
                song_list = data.get('data', {}).get('song', {}).get('list', [])
                if song_list:
                    return song_list[0]
        except Exception as e:
            logger.error(f"[QQ] Search error: {e}")
        return None

    @classmethod
    async def _get_lyric_by_mid(cls, session, song_mid):
        params = {
            'songmid': song_mid,
            'format': 'json',
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode': '0'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://y.qq.com/'
        }
        try:
            async with session.get(cls.LYRIC_API, params=params, headers=headers) as resp:
                data = await resp.json(content_type=None)
                if data.get('lyric'):
                    lrc_b64 = data['lyric']
                    lrc_text = base64.b64decode(lrc_b64).decode('utf-8')
                    return html.unescape(lrc_text)
                else:
                    logger.debug(f"[QQ] No lyric field: {data}")
        except Exception as e:
            logger.error(f"[QQ] Lyric error: {e}")
        return None
