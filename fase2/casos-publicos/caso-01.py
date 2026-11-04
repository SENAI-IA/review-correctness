import sqlite3


def list_payments(conn: sqlite3.Connection, page: int, page_size: int = 20) -> list[tuple]:
    """Paginação 1-based: page=1 devolve os primeiros page_size registros."""
    offset = page * page_size
    cur = conn.execute(
        "SELECT id, amount_cents FROM payments ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (page_size, offset),
    )
    return cur.fetchall()
