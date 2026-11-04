"""Imprime um arquivo com o número de cada linha, para citar a linha exata.

Uso: python3 numerar.py <arquivo>
"""
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(2)
for n, linha in enumerate(Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
    print(f"{n:4d}| {linha}")
