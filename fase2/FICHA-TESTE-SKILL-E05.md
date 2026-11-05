# Ficha de Teste — Skill `review-code-correctness`

**Equipe criadora:** E05  
**Equipe testadora:** E02  
**Auditora:** ____________  
**Data:** 2026-11-04

---

## Teste 1: os 4 arquivos públicos (2 pontos cada = 8)

| Arquivo | O que a skill tem que achar | Onde | Passou? |
|---------|----------------------------|------|---------|
| caso-01.py | paginação errada: `page * page_size` pula a primeira página | linha 6 | ☐ sim ☐ não |
| caso-02.py | `datetime.now()` devolve hora local, não UTC | linha 6 | ☐ sim ☐ não |
| caso-03.py | webhook aceita o mesmo evento duas vezes e credita o saldo em dobro | linhas 6-11 | ☐ sim ☐ não |
| caso-04-limpo.py | **NÃO TEM BUG** — a skill tem que dizer que está ok | nenhuma | ☐ sim ☐ não |

### Detalhes dos Bugs Esperados (do PDF):

#### caso-01.py (linha 6)
```python
offset = page * page_size  # BUG: deveria ser (page - 1) * page_size
```
- **Bug:** Com `page=1`, offset fica 20, pulando os primeiros 20 registros
- **Esperado:** página 1 → registros 1-20
- **Obtido:** página 1 → registros 21-40

#### caso-02.py (linha 6)
```python
return datetime.now()  # BUG: deveria ser datetime.now(timezone.utc)
```
- **Bug:** Docstring promete "Timestamp UTC", mas devolve hora local naive
- **Esperado:** hora UTC com tzinfo
- **Obtido:** hora local sem fuso

#### caso-03.py (linhas 6-11)
```python
conn.execute("INSERT OR REPLACE INTO webhook_events ...")  # BUG
# ...
conn.execute("UPDATE accounts SET balance_cents = balance_cents + ...")
```
- **Bug:** `INSERT OR REPLACE` não detecta duplicata; crédito roda a cada chamada
- **Esperado:** mesmo event_id → crédito uma vez só
- **Obtido:** mesmo event_id → crédito duplicado

#### caso-04-limpo.py (nenhum bug)
- Paginação correta: `(page - 1) * page_size`
- UTC correto: `datetime.now(timezone.utc)`
- Idempotência correta: `SELECT` antes do efeito, `return` se já existir
- **Se a skill inventar bug, NÃO passa**

**Parcial Teste 1:** ___/8

---

## Teste 2: a skill liga na hora certa? (1 ponto cada = 5)

| Frase | A skill deve | Acertou? |
|-------|-------------|----------|
| "revisa a correção deste arquivo" | LIGAR | ☐ sim ☐ não |
| "procura bugs de lógica aqui" | LIGAR | ☐ sim ☐ não |
| "esse código está certo?" | LIGAR | ☐ sim ☐ não |
| "explica o que essa função faz" | NÃO ligar | ☐ sim ☐ não |
| "revisa a segurança deste arquivo" | NÃO ligar | ☐ sim ☐ não |

**Parcial Teste 2:** ___/5

---

## Teste 3: casos novos da E02 (1 ponto cada, até 4)

| Arquivo | Bug esperado | Onde | Passou? | Auditora? |
|---------|--------------|------|---------|-----------|
| correctness-e02-01.py | UTC vs São Paulo: `datetime.now(timezone.utc).date()` devolve data UTC, não SP. Entre 21h-24h de SP já é dia seguinte. | linha 6 | ☐ sim ☐ não | ☐ sim ☐ não |
| correctness-e02-02.py | Gerador exaurido: `approved` é gerador, consumido na linha 4, linha 5 soma zero. | linhas 4-5 | ☐ sim ☐ não | ☐ sim ☐ não |
| correctness-e02-03.py | Ano bissexto: `date(ano+1, 2, 29)` quebra para quem assinou em 29/02. | linha 6 | ☐ sim ☐ não | ☐ sim ☐ não |
| correctness-e02-04-limpo.py | **NENHUM** (caso limpo): paginação 0-based, datetime local para recibo, INSERT OR REPLACE em config. | nenhuma | ☐ sim ☐ não | ☐ sim ☐ não |

### Detalhes dos Casos Novos:

#### correctness-e02-01.py
```python
def business_day() -> date:
    """Dia do fechamento de caixa, no fuso de São Paulo (UTC-3)."""
    return datetime.now(timezone.utc).date()  # BUG: usa UTC, não SP
```
- Às 22h30 de SP (dia 4) → UTC já é 01h30 (dia 5) → caixa fecha no dia errado

#### correctness-e02-02.py
```python
approved = (p for p in payments if p["status"] == "approved")  # gerador
count = sum(1 for _ in approved)  # consome tudo
total = sum(p["amount_cents"] for p in approved)  # gerador vazio → 0
```
- Com 2 pagamentos de 10 cada: `(2, 0)` em vez de `(2, 20)`

#### correctness-e02-03.py
```python
return date(started_on.year + 1, started_on.month, started_on.day)  # BUG
```
- `started_on = date(2024, 2, 29)` → `date(2025, 2, 29)` → ValueError

#### correctness-e02-04-limpo.py (caso limpo)
- `page * page_size` está CERTO porque docstring diz 0-based
- `datetime.now()` está CERTO porque é "hora local do terminal"
- `INSERT OR REPLACE` está CERTO porque é config, sem efeito colateral

**Parcial Teste 3:** ___/4

---

## Totalização

| Teste | Pontos |
|-------|--------|
| Teste 1 (arquivos públicos) | ___/8 |
| Teste 2 (gatilhos) | ___/5 |
| Teste 3 (casos novos) | ___/4 |
| **TOTAL para a criadora (E05)** | **___/17** |
| Pontos da testadora (E02) — Teste 3 falhados | ___ |

---

## Instruções para Preencher

1. **Teste 1:** Para cada arquivo, abrir sessão nova e dizer "revisa a correção deste arquivo"
   - Marcar ✅ se achou o bug NA LINHA CERTA
   - Arquivo limpo: marcar ✅ se NÃO inventou bug

2. **Teste 2:** Para cada frase, verificar se a skill foi carregada
   - LIGAR = skill apareceu no painel/log
   - NÃO ligar = skill não foi ativada

3. **Teste 3:** Para cada caso novo:
   - Marcar ✅ se achou o bug na linha certa (ou não inventou bug no limpo)
   - Auditora precisa aceitar que o bug é real e do tema
