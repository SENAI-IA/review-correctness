import sqlite3
from datetime import datetime, timezone


def list_payments(conn: sqlite3.Connection, page: int, page_size: int = 20) -> list[tuple]:
    offset = (page - 1) * page_size
    cur = conn.execute(
        "SELECT id, amount_cents FROM payments ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (page_size, offset),
    )
    return cur.fetchall()


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def handle_webhook(conn: sqlite3.Connection, event_id: str, payment_id: str, status: str) -> None:
    seen = conn.execute("SELECT 1 FROM webhook_events WHERE event_id = ?", (event_id,)).fetchone()
    if seen:
        return
    conn.execute("INSERT INTO webhook_events (event_id, payment_id, status) VALUES (?, ?, ?)", (event_id, payment_id, status))
    if status == "captured":
        conn.execute(
            "UPDATE accounts SET balance_cents = balance_cents + (SELECT amount_cents FROM payments WHERE id = ?) WHERE id = (SELECT account_id FROM payments WHERE id = ?)",
            (payment_id, payment_id),
        )
    conn.commit()
