import json
from typing import Iterable, List, Optional


def parse_urls(raw) -> List[str]:
    """photos_url is stored as a JSON string in the DB; return it as a list of URLs."""
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(u) for u in raw]
    try:
        parsed = json.loads(raw)
    except (TypeError, ValueError):
        return [str(raw)]
    if isinstance(parsed, list):
        return [str(u) for u in parsed]
    return [str(parsed)] if parsed else []


def removed_urls(old_raw, new_urls: Optional[Iterable[str]]) -> List[str]:
    """URLs that were in old_raw but are no longer in new_urls."""
    keep = set(new_urls or [])
    return [u for u in parse_urls(old_raw) if u not in keep]
