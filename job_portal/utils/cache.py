import hashlib
from urllib.parse import urlencode


def generate_cache_key(prefix: str, request) -> str:
    """
    Generate a unique cache key based on:
    - endpoint prefix
    - sorted query parameters
    """

    query_params = request.GET.dict()

    # Sort parameters for consistency
    sorted_params = dict(sorted(query_params.items()))

    encoded_params = urlencode(sorted_params)

    raw_key = f"{prefix}:{encoded_params}"

    # Hash to avoid extremely long keys
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest()

    return f"{prefix}:{hashed_key}"