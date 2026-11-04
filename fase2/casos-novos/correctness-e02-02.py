def summarize(payments: list[dict]) -> tuple[int, int]:
    """Devolve (quantidade, soma em centavos) dos pagamentos aprovados."""
    approved = (p for p in payments if p["status"] == "approved")
    count = sum(1 for _ in approved)
    total = sum(p["amount_cents"] for p in approved)
    return count, total
