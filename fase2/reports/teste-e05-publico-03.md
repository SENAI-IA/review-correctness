<!-- skill disparou: sim -->
## Revisão de correção: `caso-03.py`

**Resultado:** 1 problema (1 alta).

### 1. [Alta] Webhook não é idempotente - crédito duplicado (linhas 6-11)
**Lente:** estado
**O que acontece:** A docstring diz que "o adquirente pode reenviar o mesmo evento", mas `INSERT OR REPLACE` não detecta duplicata: sobrescreve a linha e segue para o UPDATE do saldo. O crédito é aplicado a cada chamada.
**Cenário:** `handle_webhook(conn, "evt_1", "pay_1", "captured")` chamado 2 vezes para pagamento de 10000 centavos → saldo fica +20000; esperado +10000.
**Correção:**
```diff
- conn.execute(
-     "INSERT OR REPLACE INTO webhook_events (event_id, payment_id, status) VALUES (?, ?, ?)",
-     (event_id, payment_id, status),
- )
+ cur = conn.execute(
+     "INSERT OR IGNORE INTO webhook_events (event_id, payment_id, status) VALUES (?, ?, ?)",
+     (event_id, payment_id, status),
+ )
+ if cur.rowcount == 0:
+     return  # evento já processado
```
**Teste:** Chamar `handle_webhook` duas vezes com mesmo event_id e verificar que saldo aumentou apenas uma vez.
**Confiança:** por leitura

### Verificado sem problemas
- O valor vem da tabela payments, não do payload (seguro).
- Se payment_id não existir, UPDATE não altera nada (não há crédito em conta errada).

### Fora do escopo
- Dois eventos diferentes (event_id distintos) para o mesmo payment_id também creditam duas vezes. Isso depende da regra de negócio.
