# Caso novo: correctness-e02-04-limpo

Quem criou: equipe E02   Testa a skill de: equipe ____________

**Arquivo:** `casos-novos/correctness-e02-04-limpo.py`

**Bug esperado:** nenhum: caso limpo. `page * page_size` está certo porque o contrato é 0-based (linha 6); `datetime.now()` local é o pedido da docstring (hora do terminal no recibo); `INSERT OR REPLACE` numa tabela de configuração sem efeito colateral é exatamente "gravar de novo só atualiza". Verificado executando.

**Por que é do tema:** testa falso positivo: imita os 3 bugs dos casos públicos, mas cada linha cumpre o seu contrato. Skill que só decorou padrão inventa achado.

**Pedido usado:** "revisa a correção deste arquivo"

**Resultado:** ____ (passou / falhou). Linha citada pela skill: ___

**Aceite da auditora:** ( ) bug real e do tema  ( ) rejeitado, motivo: ___
