import requests
import html
import base64
import json

def test_qq(keyword):
    headers = {
        'Referer': 'https://y.qq.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # 1. Search
    print(f"Searching QQ for: {keyword}")
    search_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    params = {
        'w': keyword,
        'p': 1,
        'n': 1,
        'format': 'json'
    }
    try:
        resp = requests.get(search_url, params=params, headers=headers)
        data = resp.json()
        
        song_list = data.get('data', {}).get('song', {}).get('list', [])
        if not song_list:
            print("QQ: No songs found")
            return
            
        song = song_list[0]
        song_mid = song['songmid']
        song_id = song['songid']
        print(f"QQ: Found {song['songname']} - {song_mid}")
        
        # 2. Get Lyrics
        lyric_url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"
        lrc_params = {
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
        # QQ Lyric API requires Referer
        lrc_resp = requests.get(lyric_url, params=lrc_params, headers=headers)
        lrc_data = lrc_resp.json()
        
        if lrc_data.get('lyric'):
            # QQ returns Base64 encoded lyric
            lrc_b64 = lrc_data['lyric']
            lrc_text = base64.b64decode(lrc_b64).decode('utf-8')
            # It usually contains HTML entities like &#58; 
            lrc_text = html.unescape(lrc_text)
            print("\nQQ Lyric Preview:")
            print(lrc_text[:100])
        else:
            print("QQ: No lyric field in response", lrc_data)
            
    except Exception as e:
        print(f"QQ Error: {e}")

if __name__ == "__main__":
    test_qq("香水有毒")
