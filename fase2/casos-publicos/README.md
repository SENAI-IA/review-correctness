# Casos públicos: review-correctness

Toda skill `review-correctness` precisa passar nestes 4 casos. Pedido padrão: "revisa a correção deste arquivo" (ou "procura bugs de lógica").

| Caso | Arquivo | Bug esperado (linha) | Passa se |
|---|---|---|---|
| 01 | `caso-01.py` | off-by-one na paginação 1-based: `page * page_size` pula a primeira página (linha 6) | achado cita linha 5 a 7 e explica o pulo |
| 02 | `caso-02.py` | `datetime.now()` devolve hora local sem tzinfo, não UTC (linha 6); `is_expired` quebra na troca de fuso | achado cita linha 5 a 7 e fala de naive/UTC |
| 03 | `caso-03.py` | webhook sem idempotência: `INSERT OR REPLACE` aceita o mesmo `event_id` de novo e credita o saldo duas vezes (linhas 6 a 11) | achado cita o INSERT OR REPLACE ou o crédito duplicado |
| 04 | `caso-04-limpo.py` | nenhum | relatório sem achado de severidade média ou maior |

Pontuação: +2 por caso passado. Achado sem linha não conta.
