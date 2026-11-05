<!-- skill disparou: sim -->
## Revisão de correção: `correctness-e02-01.py`

**Resultado:** 1 problema (1 alta).

### 1. [Alta] Fuso errado - UTC em vez de São Paulo (linha 6)
**Lente:** data/fuso/locale
**O que acontece:** A docstring promete "Dia do fechamento de caixa, no fuso de São Paulo (UTC-3)", mas `datetime.now(timezone.utc).date()` devolve a data em UTC, não em São Paulo. Entre 21h e 24h de São Paulo, já é o dia seguinte em UTC.
**Cenário:** São Paulo 22:30 do dia 4 (UTC 01:30 do dia 5) → `business_day()` retorna `date(2026, 11, 5)`; esperado `date(2026, 11, 4)`. O caixa fecha no dia errado.
**Correção:**
```diff
+ from zoneinfo import ZoneInfo

def business_day() -> date:
    """Dia do fechamento de caixa, no fuso de São Paulo (UTC-3, sem horário de verão)."""
-   return datetime.now(timezone.utc).date()
+   return datetime.now(ZoneInfo("America/Sao_Paulo")).date()
```
**Teste:** Simular 22:30 de São Paulo e verificar que `business_day()` retorna o dia em SP, não em UTC.
**Confiança:** por leitura (depende do horário do teste)

### Verificado sem problemas
- `is_same_business_day`: a comparação de datas está correta, dado que `business_day()` esteja certo.
