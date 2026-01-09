from cachetools import TTLCache, LRUCache
import asyncio
from functools import wraps

# Simple in-memory cache
# TTL: 1 hour, Max size: 1000 items
cache = TTLCache(maxsize=1000, ttl=3600)

def async_cache(func):
    """Decorator to cache async function results."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Create a key based on function name and arguments
        key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
        if key in cache:
            return cache[key]
        
        result = await func(*args, **kwargs)
        
        # Only cache if result is not None
        if result:
            cache[key] = result
        return result
    return wrapper
