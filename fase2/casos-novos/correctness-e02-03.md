# Caso novo: correctness-e02-03

Quem criou: equipe E02   Testa a skill de: equipe ____________

**Arquivo:** `casos-novos/correctness-e02-03.py`

**Bug esperado:** linha 6: para quem assinou em 29/02, `date(ano + 1, 2, 29)` levanta ValueError (day is out of range for month; reproduzido com 2024-02-29). Falta tratar o ano não bissexto.

**Por que é do tema:** borda de data: ano bissexto.

**Pedido usado:** "revisa a correção deste arquivo"

**Resultado:** ____ (passou / falhou). Linha citada pela skill: ___

**Aceite da auditora:** ( ) bug real e do tema  ( ) rejeitado, motivo: ___
