import sqlite3
from datetime import datetime


def list_page(conn: sqlite3.Connection, page: int, page_size: int = 20) -> list[tuple]:
    """Paginação 0-based (contrato do app mobile): page=0 devolve os primeiros page_size."""
    offset = page * page_size
    return conn.execute(
        "SELECT id FROM receipts ORDER BY id LIMIT ? OFFSET ?", (page_size, offset)
    ).fetchall()


def receipt_header(store: str) -> str:
    """Cabeçalho do recibo impresso no caixa, com a hora local do terminal."""
    return f"{store} - {datetime.now():%d/%m/%Y %H:%M}"


def save_terminal_setting(conn: sqlite3.Connection, key: str, value: str) -> None:
    """Grava a configuração do terminal; gravar de novo a mesma chave só atualiza o valor."""
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
