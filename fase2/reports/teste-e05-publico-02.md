<!-- skill disparou: sim -->
## Revisão de correção: `caso-02.py`

**Resultado:** 1 problema (1 média).

### 1. [Média] datetime naive em vez de UTC (linha 6)
**Lente:** data/fuso/locale
**O que acontece:** A docstring promete "Timestamp UTC para gravar em created_at", mas `datetime.now()` devolve hora local naive (sem tzinfo). Em servidor no fuso -03, às 21:00 UTC o retorno é 18:00 local.
**Cenário:** Servidor em America/Sao_Paulo às 21:00 UTC → `now_utc()` retorna `datetime(2026, 11, 4, 18, 0, 0)` sem tzinfo; esperado `datetime(2026, 11, 4, 21, 0, 0, tzinfo=timezone.utc)`.
**Correção:**
```diff
- return datetime.now()
+ return datetime.now(timezone.utc)
```
E adicionar `from datetime import timezone` no import.
**Teste:** `assert now_utc().tzinfo == timezone.utc`
**Confiança:** por leitura

### Verificado sem problemas
- `is_expired`: a comparação `>` está correta para "expira após o TTL".

### Fora do escopo
- Se `created_at` existente foi gravado sem fuso, comparar com o novo `now_utc()` aware causará TypeError ou resultado errado.
