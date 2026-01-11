import aiohttp
import asyncio
import os
import sys

# Usage: NETEASE_COOKIE="xxx" python3 test_netease_auth.py
async def test_netease():
    cookie = os.getenv("NETEASE_COOKIE")
    if not cookie:
        print("❌ Error: Please set NETEASE_COOKIE environment variable.")
        print("Example: export NETEASE_COOKIE='MUSIC_U=...'; python3 test_netease_auth.py")
        return

    print(f"🔒 Testing with Cookie length: {len(cookie)}")
    print(f"🍪 Cookie preview: {cookie[:20]}...")

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'origin': 'https://music.163.com',
        'referer': 'https://music.163.com',
        'cookie': cookie
    }
    
    url = "http://music.163.com/api/search/get/web"
    params = {
        's': '香水有毒',
        'type': 1,
        'offset': 0,
        'total': 'true',
        'limit': 1
    }

    async with aiohttp.ClientSession() as session:
        print(f"\n📡 Sending request to {url}...")
        try:
            async with session.post(url, data=params, headers=headers) as resp:
                print(f"⬅️ Response Status: {resp.status}")
                print(f"📄 Content-Type: {resp.content_type}")
                
                content = await resp.text()
                print(f"\n📜 Response Body Preview (First 500 chars):")
                print("-" * 40)
                print(content[:500])
                print("-" * 40)
                
                if resp.status == 200:
                    try:
                        data = await resp.json(content_type=None)
                        songs = data.get('result', {}).get('songs', [])
                        if songs:
                            print(f"\n✅ SUCCESS! Found song: {songs[0]['name']} (ID: {songs[0]['id']})")
                            print("Context: The cookie is working and IP is allowed.")
                        else:
                            print("\n⚠️ WARNING: Request succeeded but no songs found.")
                            print("Context: Search logic might be returning empty, or account is limited.")
                    except:
                        print("\n❌ FAILURE: Response is not valid JSON.")
                        if "verify" in content or "Cheating" in content:
                            print("Reason: IP blocked or CAPTCHA required (Anticheat triggered).")
        except Exception as e:
            print(f"\n❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_netease())
