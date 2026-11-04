from datetime import date, datetime, timezone


def business_day() -> date:
    """Dia do fechamento de caixa, no fuso de São Paulo (UTC-3, sem horário de verão)."""
    return datetime.now(timezone.utc).date()


def is_same_business_day(paid_at: datetime) -> bool:
    return paid_at.date() == business_day()
