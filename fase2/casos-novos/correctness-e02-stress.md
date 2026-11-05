# Caso Stress: correctness-e02-stress

Quem criou: equipe E02   Testa a skill de: equipe ____________

**Arquivo:** `casos-novos/correctness-e02-stress.py`

## Bugs Esperados (5 bugs)

### Bug 1 - Linha 13-14: datetime naive em filtro UTC
```python
start = datetime(date.year, date.month, date.day, 0, 0, 0)  # naive!
end = datetime(date.year, date.month, date.day, 23, 59, 59)  # naive!
```
- **Problema:** Docstring diz "UTC", mas cria datetime naive
- **Tema:** data/fuso

### Bug 2 - Linha 24: float em cálculo de dinheiro + truncamento
```python
return int(amount_cents * fee_percent / 100)
```
- **Problema:** `fee_percent` é float, `int()` trunca (não arredonda). `int(19.99)` = 19, não 20.
- **Cenário:** `calculate_fee(999, 2.5)` → `int(24.975)` = 24, mas deveria ser 25 (arredondamento)
- **Tema:** lógica/dinheiro

### Bug 3 - Linhas 33-37: rateio perde centavos
```python
for p in partners:
    share = int(total_cents * p["weight"] / total_weight)
    result[p["id"]] = share
```
- **Problema:** Soma das parcelas < total (resto perdido)
- **Cenário:** `split_revenue(100, [{id:"A", weight:1}, {id:"B", weight:1}, {id:"C", weight:1}])` → {"A":33, "B":33, "C":33} = 99, não 100
- **Tema:** lógica/dinheiro

### Bug 4 - Linha 95: timedelta não importado
```python
cutoff = datetime.now() - timedelta(hours=ttl_hours)
```
- **Problema:** `timedelta` não está no import, vai dar NameError
- **Cenário:** Chamar `expire_pending_transactions()` → NameError
- **Tema:** lógica

### Bug 5 - Linha 95: datetime.now() naive vs banco UTC
```python
cutoff = datetime.now() - timedelta(hours=ttl_hours)
```
- **Problema:** Mesmo se importar timedelta, `datetime.now()` é hora local. Se banco está em UTC, comparação está errada.
- **Tema:** data/fuso

## Resumo

| # | Linha | Bug | Tema | Severidade |
|---|-------|-----|------|------------|
| 1 | 13-14 | datetime naive em filtro UTC | data/fuso | média |
| 2 | 24 | float + truncamento em taxa | dinheiro | alta |
| 3 | 33-37 | rateio perde resto | dinheiro | crítica |
| 4 | 95 | timedelta não importado | lógica | alta |
| 5 | 95 | datetime.now() naive | data/fuso | média |

**Total:** 5 bugs

**Por que é stress:** Arquivo maior, múltiplos bugs de temas diferentes, alguns sutis (truncamento vs arredondamento), um erro de import que pode mascarar outro bug na mesma linha.

---

**Resultado:** ____ bugs encontrados de 5

**Aceite da auditora:** ( ) bugs reais e do tema  ( ) rejeitado, motivo: ___
