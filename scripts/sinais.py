"""Lista linhas suspeitas de bug de correção em arquivos .py (pistas, não achados).

Uso: python3 sinais.py <arquivo-ou-pasta> [...]
Saída: arquivo:linha: [sinal] trecho
"""
import re
import sys
from pathlib import Path

SINAIS = [
    ("datetime naive", re.compile(r"datetime\.(now|today)\(\s*\)|\.utcnow\(|date\.today\(\)|fromtimestamp\([^,()]*\)|\.strptime\(")),
    ("tz replace", re.compile(r"\.replace\(\s*tzinfo\s*=")),
    ("idempotência", re.compile(r"INSERT\s+OR\s+REPLACE|REPLACE\s+INTO|ON\s+CONFLICT.*DO\s+UPDATE", re.I)),
    ("paginação", re.compile(r"\bpage\s*\*\s*\w+|\w+\s*\*\s*page\b")),
    ("float/round em quantia", re.compile(r"\bfloat\(|\bround\(|int\([^)]*\*\s*100|\b(amount|valor|saldo|balance|price|preco|total)\w*\s*:\s*float")),
    ("default mutável", re.compile(r"def \w+\(.*=\s*(\[\]|\{\}|set\(\))")),
    ("erro engolido", re.compile(r"except\s*(Exception)?\s*:\s*(pass)?\s*$")),
    ("retorno de falha", re.compile(r"return\s+(None|-1|False)\s*$")),
    ("is com literal", re.compile(r"\bis\s+(not\s+)?(\d+|['\"])")),
]


def arquivos(alvos):
    for alvo in map(Path, alvos):
        yield from (sorted(alvo.rglob("*.py")) if alvo.is_dir() else [alvo])


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    total = 0
    for arq in arquivos(sys.argv[1:]):
        for n, linha in enumerate(arq.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for nome, rx in SINAIS:
                if nome == "paginação" and re.search(r"page\s*-\s*1", linha):
                    continue
                if rx.search(linha):
                    print(f"{arq}:{n}: [{nome}] {linha.strip()}")
                    total += 1
    print(f"# {total} sinal(is); confirme cada um no código antes de reportar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
