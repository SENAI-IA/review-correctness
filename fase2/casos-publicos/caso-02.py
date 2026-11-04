from datetime import datetime


def now_utc() -> datetime:
    """Timestamp UTC para gravar em created_at."""
    return datetime.now()


def is_expired(created_at: datetime, ttl_seconds: int) -> bool:
    return (now_utc() - created_at).total_seconds() > ttl_seconds
