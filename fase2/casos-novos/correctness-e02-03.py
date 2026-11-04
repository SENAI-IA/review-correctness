from datetime import date


def renew_subscription(started_on: date) -> date:
    """Data de renovação: o mesmo dia e mês, um ano depois."""
    return date(started_on.year + 1, started_on.month, started_on.day)
