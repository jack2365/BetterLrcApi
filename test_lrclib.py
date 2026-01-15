import asyncio
import aiohttp
from services.lrclib import LrclibProvider

async def test_lrclib():
    # Test cases: specific English songs known to be on Lrclib
    test_cases = [
        "Thinking Out Loud Ed Sheeran",
        "Shape of You"
    ]

    print("=== Testing LrclibProvider ===")
    
    for keyword in test_cases:
        print(f"\nSearching for: {keyword}")
        lrc = await LrclibProvider.get_lyrics(keyword)
        
        if lrc:
            print(f"✅ Success! Length: {len(lrc)} chars")
            print(f"Preview: {lrc[:100]}...")
        else:
            print("❌ Failed to find lyrics")

if __name__ == "__main__":
    asyncio.run(test_lrclib())
