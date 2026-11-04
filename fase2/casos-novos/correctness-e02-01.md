# Caso novo: correctness-e02-01

Quem criou: equipe E02   Testa a skill de: equipe ____________

**Arquivo:** `casos-novos/correctness-e02-01.py`

**Bug esperado:** linha 6: `datetime.now(timezone.utc).date()` devolve a data em UTC, não em São Paulo como a docstring promete. Entre 21h e 24h de SP já é o dia seguinte em UTC: às 22h30 do dia 4 em SP a função devolve dia 5 (reproduzido), e o caixa fecha no dia errado.

**Por que é do tema:** data e fuso: o datetime é aware, mas no fuso errado para a regra.

**Pedido usado:** "revisa a correção deste arquivo"

**Resultado:** ____ (passou / falhou). Linha citada pela skill: ___

**Aceite da auditora:** ( ) bug real e do tema  ( ) rejeitado, motivo: ___
