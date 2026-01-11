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
            
            # 3. Download Lyrics (Pass song_hash for fallback)
            lrc_content = await cls._download_lyrics(
                session, 
                candidate['id'], 
                candidate['accesskey'],
                song_hash=song_hash
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
            # Try to add headers to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
            }
            async with session.get(cls.SEARCH_API, params=params, headers=headers) as resp:
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
                    return data['candidates'][0]
        except Exception as e:
            logger.error(f"[Kugou] Lyric search error: {e}")
        return None

    @classmethod
    async def _download_lyrics(cls, session, lrc_id, access_key, song_hash=None):
        # 1. Try Primary PC API
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
                try:
                    data = json.loads(text_content)
                except json.JSONDecodeError:
                    data = None

                if isinstance(data, dict) and data.get('status') == 200 and data.get('content'):
                    decoded_content = base64.b64decode(data['content']).decode('utf-8')
                    return decoded_content
                else:
                    logger.warning(f"[Kugou] Primary download failed (Status: {data.get('status') if isinstance(data, dict) else 'Unknown'}).")
        except Exception as e:
            logger.error(f"[Kugou] Primary download error: {e}")
            
        # 2. Fallback: Secondary Mobile Endpoint (Known to work in some restricted regions)
        if song_hash:
            logger.info("[Kugou] Trying secondary mobile endpoint...")
            return await cls._download_simple(session, song_hash)
        
        return None

    @classmethod
    async def _download_simple(cls, session, song_hash):
        # http://mobilecdn.kugou.com/new/app/i/krc.php?cmd=100&hash={hash}&timelength=999999
        url = "http://mobilecdn.kugou.com/new/app/i/krc.php"
        params = {
            'cmd': '100',
            'hash': song_hash,
            'timelength': '999999'
        }
        try:
            async with session.get(url, params=params) as resp:
                text = await resp.text()
                # If text is valid lyrics (simple heuristic: contains time tags or is long enough)
                if len(text) > 20 and ("[" in text or "{" not in text[:5]):
                     return text
                else:
                     logger.warning(f"[Kugou] Simple endpoint returned non-lyrics: {text[:100]}")
        except Exception as e:
            logger.error(f"[Kugou] Simple endpoint error: {e}")
        return None
