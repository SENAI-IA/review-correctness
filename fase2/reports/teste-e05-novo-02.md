<!-- skill disparou: sim -->
## Revisão de correção: `correctness-e02-02.py`

**Resultado:** 1 problema (1 alta).

### 1. [Alta] Gerador consumido duas vezes - total sempre zero (linhas 4-5)
**Lente:** estado
**O que acontece:** `approved` é um gerador (generator expression). A linha 4 consome todo o gerador para contar. Na linha 5, o gerador já está vazio, então a soma dá zero.
**Cenário:** `summarize([{"status": "approved", "amount_cents": 10}, {"status": "approved", "amount_cents": 10}])` → retorna `(2, 0)`; esperado `(2, 20)`.
**Correção:**
```diff
def summarize(payments: list[dict]) -> tuple[int, int]:
    """Devolve (quantidade, soma em centavos) dos pagamentos aprovados."""
-   approved = (p for p in payments if p["status"] == "approved")
-   count = sum(1 for _ in approved)
-   total = sum(p["amount_cents"] for p in approved)
+   approved = [p for p in payments if p["status"] == "approved"]  # lista, não gerador
+   count = len(approved)
+   total = sum(p["amount_cents"] for p in approved)
    return count, total
```
**Teste:** `assert summarize([{"status": "approved", "amount_cents": 100}]) == (1, 100)`
**Confiança:** confirmado (executei o cenário)

### Verificado sem problemas
- Lista vazia retorna (0, 0) corretamente.
- Pagamentos não aprovados são filtrados corretamente.
