<!-- skill disparou: sim -->
## Revisão de correção: `caso-01.py`

**Resultado:** 1 problema (1 alta).

### 1. [Alta] Paginação 1-based com offset errado (linha 6)
**Lente:** borda
**O que acontece:** A docstring promete paginação 1-based (`page=1` devolve os primeiros registros), mas o cálculo `offset = page * page_size` pula a primeira página inteira.
**Cenário:** `list_payments(conn, page=1, page_size=20)` → offset = 20, devolve registros 21-40; esperado registros 1-20.
**Correção:**
```diff
- offset = page * page_size
+ offset = (page - 1) * page_size
```
**Teste:** `assert list_payments(conn, 1, 20)` retorna os primeiros 20 registros (offset 0).
**Confiança:** por leitura

### Verificado sem problemas
- Lente lógica: SELECT está correto, ORDER BY funciona.
- Lente estado: não há estado compartilhado.

### Fora do escopo
- Linha 8: `ORDER BY created_at DESC` não tem desempate; pode causar inconsistência na fronteira entre páginas se `created_at` repetir.
