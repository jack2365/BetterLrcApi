import aiohttp
import json
import base64
import logging

# Configure basic logging to stdout
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class KugouProvider:
    SEARCH_API = "http://mobilecdn.kugou.com/api/v3/search/song"
    LYRICS_SEARCH_API = "http://krcs.kugou.com/search"
    DOWNLOAD_API = "http://lyrics.kugou.com/download/lz"

    @classmethod
    async def get_lyrics(cls, keyword: str) -> str:
        """
        Main entry point: Search -> Match -> Download
        """
        async with aiohttp.ClientSession() as session:
            # 1. Search Song to get Hash
            song_info = await cls._search_song(session, keyword)
            if not song_info:
                logger.debug(f"[Kugou] No song found for {keyword}")
                return None
            
            song_hash = song_info.get('hash')
            if not song_hash:
                return None
                
            # 2. Search Lyrics Candidates via Hash
            candidate = await cls._search_lyrics_candidates(session, song_hash=song_hash)
            if not candidate:
                logger.debug(f"[Kugou] No lyrics candidates for hash {song_hash}")
                return None
            
            # 3. Download Lyrics
            lrc_content = await cls._download_lyrics(
                session, 
                candidate['id'], 
                candidate['accesskey']
            )
            return lrc_content

    @classmethod
    async def _search_song(cls, session, keyword):
        params = {
            "format": "json",
            "keyword": keyword,
            "page": 1,
            "pagesize": 1,
            "showtype": 1
        }
        try:
            async with session.get(cls.SEARCH_API, params=params) as resp:
                data = await resp.json(content_type=None)
                if data.get('status') == 1 and data.get('data', {}).get('info'):
                    return data['data']['info'][0]
        except Exception as e:
            logger.error(f"[Kugou] Search error: {e}")
        return None

    @classmethod
    async def _search_lyrics_candidates(cls, session, song_hash):
        params = {
            'ver': '1',
            'man': 'yes',
            'client': 'mobi',
            'keyword': '', # Hash usually suffices
            'duration': '',
            'hash': song_hash,
            'album_audio_id': ''
        }
        try:
            async with session.get(cls.LYRICS_SEARCH_API, params=params) as resp:
                data = await resp.json(content_type=None)
                if data.get('status') == 200 and data.get('candidates'):
                    # Pick the best candidate (usually the first one or logic based on duration score)
                    # For simplicity, pick the first one
                    return data['candidates'][0]
        except Exception as e:
            logger.error(f"[Kugou] Lyric search error: {e}")
        return None

    @classmethod
    async def _download_lyrics(cls, session, lrc_id, access_key):
        params = {
            'ver': '1',
            'client': 'pc',
            'id': lrc_id,
            'accesskey': access_key,
            'fmt': 'lrc',
            'charset': 'utf8'
        }
        try:
            async with session.get(cls.DOWNLOAD_API, params=params) as resp:
                text_content = await resp.text()
                # logger.debug(f"[Kugou] Download response: {text_content[:200]}")
                
                try:
                    data = json.loads(text_content)
                except json.JSONDecodeError:
                    logger.error(f"[Kugou] Download JSON decode error. Content type: {resp.content_type}, Text: {text_content[:100]}")
                    return None

                if data.get('status') == 200 and data.get('content'):
                    decoded_content = base64.b64decode(data['content']).decode('utf-8')
                    return decoded_content
                else:
                    logger.error(f"[Kugou] Download status failed: {data}")
        except Exception as e:
            logger.error(f"[Kugou] Download error: {e}")
        return None

