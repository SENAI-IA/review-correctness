# Caso novo: correctness-e02-02

Quem criou: equipe E02   Testa a skill de: equipe ____________

**Arquivo:** `casos-novos/correctness-e02-02.py`

**Bug esperado:** linhas 3-5: `approved` é um gerador; a linha 4 o consome inteiro e a linha 5 soma um gerador vazio. Com 2 pagamentos aprovados de 10, devolve (2, 0) em vez de (2, 20) (reproduzido).

**Por que é do tema:** estado: iterador consumido duas vezes; resultado errado sem nenhum erro.

**Pedido usado:** "revisa a correção deste arquivo"

**Resultado:** ____ (passou / falhou). Linha citada pela skill: ___

**Aceite da auditora:** ( ) bug real e do tema  ( ) rejeitado, motivo: ___
