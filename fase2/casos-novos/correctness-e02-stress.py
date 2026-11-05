"""
Sistema de processamento de pagamentos em lote.
Processa transações do dia, calcula taxas e distribui entre parceiros.
"""
from datetime import datetime, timezone
from decimal import Decimal
import sqlite3


def get_daily_transactions(conn: sqlite3.Connection, date: datetime) -> list[dict]:
    """Busca transações do dia (UTC). Retorna lista vazia se não houver."""
    start = datetime(date.year, date.month, date.day, 0, 0, 0)
    end = datetime(date.year, date.month, date.day, 23, 59, 59)
    rows = conn.execute(
        "SELECT id, amount_cents, partner_id FROM transactions WHERE created_at BETWEEN ? AND ?",
        (start.isoformat(), end.isoformat()),
    ).fetchall()
    return [{"id": r[0], "amount_cents": r[1], "partner_id": r[2]} for r in rows]


def calculate_fee(amount_cents: int, fee_percent: float) -> int:
    """Calcula taxa em centavos. fee_percent é decimal (ex: 2.5 para 2.5%)."""
    return int(amount_cents * fee_percent / 100)


def split_revenue(total_cents: int, partners: list[dict]) -> dict[str, int]:
    """
    Divide receita entre parceiros proporcionalmente ao peso.
    Soma dos valores retornados deve ser igual a total_cents.
    Exemplo: total=100, partners=[{id:"A", weight:1}, {id:"B", weight:1}] -> {"A": 50, "B": 50}
    """
    total_weight = sum(p["weight"] for p in partners)
    result = {}
    for p in partners:
        share = int(total_cents * p["weight"] / total_weight)
        result[p["id"]] = share
    return result


def process_batch(conn: sqlite3.Connection, batch_id: str, transactions: list[dict]) -> dict:
    """
    Processa lote de transações. Pode ser chamado múltiplas vezes em caso de retry.
    Retorna {success: bool, processed: int, total_fees: int}
    """
    processed = 0
    total_fees = 0
    
    for tx in transactions:
        # Verifica se já processou
        existing = conn.execute(
            "SELECT 1 FROM processed_transactions WHERE tx_id = ?", (tx["id"],)
        ).fetchone()
        
        if existing:
            continue
            
        fee = calculate_fee(tx["amount_cents"], 2.5)
        total_fees += fee
        
        # Registra processamento
        conn.execute(
            "INSERT INTO processed_transactions (tx_id, batch_id, fee_cents) VALUES (?, ?, ?)",
            (tx["id"], batch_id, fee),
        )
        
        # Credita parceiro
        conn.execute(
            "UPDATE partners SET balance_cents = balance_cents + ? WHERE id = ?",
            (tx["amount_cents"] - fee, tx["partner_id"]),
        )
        
        processed += 1
    
    conn.commit()
    return {"success": True, "processed": processed, "total_fees": total_fees}


def get_partner_statement(conn: sqlite3.Connection, partner_id: str, month: int, year: int) -> list[dict]:
    """Extrato do parceiro no mês. Mês de 1-12."""
    # Primeiro e último dia do mês
    first_day = datetime(year, month, 1)
    if month == 12:
        last_day = datetime(year + 1, 1, 1)
    else:
        last_day = datetime(year, month + 1, 1)
    
    rows = conn.execute(
        """
        SELECT t.id, t.amount_cents, t.created_at, p.fee_cents
        FROM transactions t
        JOIN processed_transactions p ON t.id = p.tx_id
        WHERE t.partner_id = ? AND t.created_at >= ? AND t.created_at < ?
        ORDER BY t.created_at
        """,
        (partner_id, first_day.isoformat(), last_day.isoformat()),
    ).fetchall()
    
    return [
        {"id": r[0], "amount": r[1], "date": r[2], "fee": r[3]}
        for r in rows
    ]


def expire_pending_transactions(conn: sqlite3.Connection, ttl_hours: int = 24) -> int:
    """Expira transações pendentes há mais de ttl_hours. Retorna quantidade expirada."""
    cutoff = datetime.now() - timedelta(hours=ttl_hours)
    cur = conn.execute(
        "UPDATE transactions SET status = 'expired' WHERE status = 'pending' AND created_at < ?",
        (cutoff.isoformat(),),
    )
    conn.commit()
    return cur.rowcount
