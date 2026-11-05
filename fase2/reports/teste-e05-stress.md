<!-- skill disparou: sim -->
## Revisão de correção: `correctness-e02-stress.py`

**Resultado:** 5 problemas (2 crítica, 2 alta, 1 média).

### 1. [Crítica] Rateio perde centavos - soma menor que total (linhas 33-37)
**Lente:** lógica/dinheiro
**O que acontece:** A docstring promete "Soma dos valores retornados deve ser igual a total_cents", mas o `int()` em cada parcela descarta o resto da divisão. A soma das partes fica menor que o total.
**Cenário:** `split_revenue(100, [{"id":"A","weight":1}, {"id":"B","weight":1}, {"id":"C","weight":1}])` → `{"A":33, "B":33, "C":33}` = 99; esperado 100. Perdeu 1 centavo.
**Correção:**
```diff
def split_revenue(total_cents: int, partners: list[dict]) -> dict[str, int]:
    total_weight = sum(p["weight"] for p in partners)
    result = {}
+   distributed = 0
    for p in partners:
        share = int(total_cents * p["weight"] / total_weight)
        result[p["id"]] = share
+       distributed += share
+   # Distribui o resto para o primeiro parceiro
+   if distributed < total_cents:
+       first_id = partners[0]["id"]
+       result[first_id] += total_cents - distributed
    return result
```
**Teste:** `assert sum(split_revenue(100, [{"id":"A","weight":1}, {"id":"B","weight":1}, {"id":"C","weight":1}]).values()) == 100`
**Confiança:** confirmado

### 2. [Alta] timedelta não importado - NameError (linha 95)
**Lente:** lógica
**O que acontece:** A função `expire_pending_transactions` usa `timedelta`, mas ele não está no import. Chamar a função levanta `NameError: name 'timedelta' is not defined`.
**Cenário:** `expire_pending_transactions(conn, 24)` → `NameError`; esperado executar sem erro.
**Correção:**
```diff
- from datetime import datetime, timezone
+ from datetime import datetime, timezone, timedelta
```
**Teste:** `expire_pending_transactions(conn, 24)` não deve levantar NameError.
**Confiança:** confirmado

### 3. [Alta] Float em cálculo de taxa com truncamento (linha 24)
**Lente:** lógica/dinheiro
**O que acontece:** `fee_percent` é float e `int()` trunca (não arredonda). Valores com casas decimais perdem centavos.
**Cenário:** `calculate_fee(999, 2.5)` → `int(999 * 2.5 / 100)` = `int(24.975)` = 24; esperado 25 (arredondamento comercial).
**Correção:**
```diff
def calculate_fee(amount_cents: int, fee_percent: float) -> int:
-   return int(amount_cents * fee_percent / 100)
+   return round(amount_cents * fee_percent / 100)
```
Ou melhor, usar Decimal:
```python
from decimal import Decimal, ROUND_HALF_UP
def calculate_fee(amount_cents: int, fee_percent: Decimal) -> int:
    return int((Decimal(amount_cents) * fee_percent / 100).quantize(1, ROUND_HALF_UP))
```
**Teste:** `assert calculate_fee(999, 2.5) == 25`
**Confiança:** confirmado

### 4. [Média] datetime naive em filtro UTC (linhas 13-14)
**Lente:** data/fuso/locale
**O que acontece:** A docstring diz "Busca transações do dia (UTC)", mas `start` e `end` são datetime naive (sem tzinfo). Se o banco armazena em UTC com fuso, a comparação pode dar resultado errado ou TypeError.
**Cenário:** Servidor em -03, transação às 01:00 UTC do dia 5 → `start` é `2026-11-05 00:00:00` naive, que pode ser interpretado como hora local (04:00 UTC do dia 5), perdendo a transação.
**Correção:**
```diff
def get_daily_transactions(conn: sqlite3.Connection, date: datetime) -> list[dict]:
-   start = datetime(date.year, date.month, date.day, 0, 0, 0)
-   end = datetime(date.year, date.month, date.day, 23, 59, 59)
+   start = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc)
+   end = datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=timezone.utc)
```
**Teste:** Verificar que transação às 01:00 UTC é encontrada.
**Confiança:** por leitura

### 5. [Média] datetime.now() naive em expiração (linha 95)
**Lente:** data/fuso/locale
**O que acontece:** Mesmo corrigindo o import de `timedelta`, `datetime.now()` devolve hora local naive. Se `created_at` no banco está em UTC, a comparação está errada por ±N horas dependendo do fuso do servidor.
**Cenário:** Servidor em -03, transação criada há 22h UTC. `datetime.now()` devolve hora local (3h a menos). Cutoff fica 3h adiantado, transação expira antes do tempo.
**Correção:**
```diff
- cutoff = datetime.now() - timedelta(hours=ttl_hours)
+ cutoff = datetime.now(timezone.utc) - timedelta(hours=ttl_hours)
```
**Teste:** Verificar que transação com exatamente 24h não é expirada (deve esperar > 24h).
**Confiança:** por leitura

---

### Verificado sem problemas
- `process_batch`: checagem de duplicata com SELECT antes do efeito está correta para retry. INSERT e UPDATE vão no mesmo commit.
- `get_partner_statement`: tratamento de mês 12 → ano+1 está correto.

### Fora do escopo
- Linhas 52-66: race condition se duas chamadas simultâneas processarem o mesmo lote. Depende de isolamento do banco.
- Import de `Decimal` não usado (linha 5).

---

## Resumo

| # | Linha | Bug | Severidade | Encontrado? |
|---|-------|-----|------------|-------------|
| 1 | 33-37 | Rateio perde resto | crítica | ✅ |
| 2 | 95 | timedelta não importado | alta | ✅ |
| 3 | 24 | float + truncamento | alta | ✅ |
| 4 | 13-14 | datetime naive em filtro UTC | média | ✅ |
| 5 | 95 | datetime.now() naive | média | ✅ |

**Total encontrado: 5/5 bugs** ✅
