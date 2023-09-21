from django.core.cache import cache


def cache_decorator(cache_key):
    def custom_cache(func):
        def wrapper(*args, **kwargs):

            cached_data = cache.get(cache_key)
            if not cached_data:
                result = func(*args, **kwargs)
                cache.set(
                    cache_key,
                    result,
                    timeout=60 * 60 * 24,  # session will be stored for a day
                )
                return result
            
            return cached_data

        return wrapper
    return custom_cache