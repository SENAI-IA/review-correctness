<!-- skill disparou: sim -->
## Revisão de correção: `correctness-e02-03.py`

**Resultado:** 1 problema (1 alta).

### 1. [Alta] Ano bissexto não tratado - ValueError em 29/02 (linha 6)
**Lente:** borda
**O que acontece:** Para quem assinou em 29 de fevereiro (ano bissexto), renovar um ano depois levanta exceção porque o próximo ano pode não ser bissexto.
**Cenário:** `renew_subscription(date(2024, 2, 29))` → `date(2025, 2, 29)` → `ValueError: day is out of range for month`; esperado `date(2025, 2, 28)` ou `date(2025, 3, 1)`.
**Correção:**
```diff
def renew_subscription(started_on: date) -> date:
    """Data de renovação: o mesmo dia e mês, um ano depois."""
-   return date(started_on.year + 1, started_on.month, started_on.day)
+   try:
+       return date(started_on.year + 1, started_on.month, started_on.day)
+   except ValueError:
+       # 29/02 em ano não bissexto → 28/02
+       return date(started_on.year + 1, started_on.month, 28)
```
**Teste:** `assert renew_subscription(date(2024, 2, 29)) == date(2025, 2, 28)`
**Confiança:** confirmado (executei o cenário)

### Verificado sem problemas
- Outros meses funcionam corretamente.
- 31 de janeiro + 1 ano funciona (janeiro sempre tem 31 dias).
