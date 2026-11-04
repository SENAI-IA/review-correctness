import sqlite3


def handle_webhook(conn: sqlite3.Connection, event_id: str, payment_id: str, status: str) -> None:
    """Processa um evento do adquirente. O adquirente pode reenviar o mesmo evento."""
    conn.execute(
        "INSERT OR REPLACE INTO webhook_events (event_id, payment_id, status) VALUES (?, ?, ?)",
        (event_id, payment_id, status),
    )
    if status == "captured":
        conn.execute("UPDATE accounts SET balance_cents = balance_cents + (SELECT amount_cents FROM payments WHERE id = ?) WHERE id = (SELECT account_id FROM payments WHERE id = ?)", (payment_id, payment_id))
    conn.commit()
