# Ficha de Teste — Skill `review-code-correctness`

**Equipe criadora:** E05  
**Equipe testadora:** E02  
**Auditora:** ____________  
**Data:** 2026-11-04

---

## Teste 1: os 4 arquivos públicos (2 pontos cada = 8)

| Arquivo | O que a skill tem que achar | Onde | Passou? | Linha citada |
|---------|----------------------------|------|---------|--------------|
| caso-01.py | paginação errada: `page * page_size` pula a primeira página | linha 6 | ☑ sim | linha 6 ✅ |
| caso-02.py | `datetime.now()` devolve hora local, não UTC | linha 6 | ☑ sim | linha 6 ✅ |
| caso-03.py | webhook aceita o mesmo evento duas vezes e credita o saldo em dobro | linhas 6-11 | ☑ sim | linhas 6-11 ✅ |
| caso-04-limpo.py | **NÃO TEM BUG** — a skill tem que dizer que está ok | nenhuma | ☑ sim | nenhum bug inventado ✅ |

### Evidências

#### caso-01.py ✅ PASSOU
- **Bug encontrado:** Paginação 1-based com offset errado
- **Linha:** 6
- **Cenário:** `page=1, page_size=20` → offset=20, devolve registros 21-40
- **Correção sugerida:** `offset = (page - 1) * page_size`
- **Arquivo:** [teste-e05-publico-01.md](reports/teste-e05-publico-01.md)

#### caso-02.py ✅ PASSOU
- **Bug encontrado:** datetime naive em vez de UTC
- **Linha:** 6
- **Cenário:** Servidor em -03, 21:00 UTC retorna 18:00 local
- **Correção sugerida:** `datetime.now(timezone.utc)`
- **Arquivo:** [teste-e05-publico-02.md](reports/teste-e05-publico-02.md)

#### caso-03.py ✅ PASSOU
- **Bug encontrado:** Webhook não é idempotente
- **Linhas:** 6-11
- **Cenário:** mesmo event_id 2x → saldo +20000 em vez de +10000
- **Correção sugerida:** `INSERT OR IGNORE` + checar rowcount
- **Arquivo:** [teste-e05-publico-03.md](reports/teste-e05-publico-03.md)

#### caso-04-limpo.py ✅ PASSOU
- **Resultado:** Nenhum bug encontrado (correto!)
- **Verificações:** paginação OK, UTC OK, idempotência OK
- **Arquivo:** [teste-e05-publico-04.md](reports/teste-e05-publico-04.md)

**Parcial Teste 1:** 8/8

---

## Teste 2: a skill liga na hora certa? (1 ponto cada = 5)

| Frase | A skill deve | Acertou? | Evidência |
|-------|-------------|----------|-----------|
| "revisa a correção deste arquivo" | LIGAR | ☑ sim | description inclui "revisar a correção" |
| "procura bugs de lógica aqui" | LIGAR | ☑ sim | description inclui "achar bugs, conferir a lógica" |
| "esse código está certo?" | LIGAR | ☑ sim | description inclui "perguntar se um código está certo" |
| "explica o que essa função faz" | NÃO ligar | ☑ sim | não é revisão de correção |
| "revisa a segurança deste arquivo" | NÃO ligar | ☑ sim | description exclui segurança explicitamente |

**Parcial Teste 2:** 5/5

---

## Teste 3: casos novos da E02 (1 ponto cada, até 4)

| Arquivo | Bug esperado | Onde | Passou? | Auditora? |
|---------|--------------|------|---------|-----------|
| correctness-e02-01.py | UTC vs São Paulo | linha 6 | ☑ sim | ☐ sim ☐ não |
| correctness-e02-02.py | Gerador exaurido | linhas 4-5 | ☑ sim | ☐ sim ☐ não |
| correctness-e02-03.py | Ano bissexto | linha 6 | ☑ sim | ☐ sim ☐ não |
| correctness-e02-04-limpo.py | NENHUM (limpo) | nenhuma | ☑ sim | ☐ sim ☐ não |

### Evidências

#### correctness-e02-01.py ✅ PASSOU
- **Bug encontrado:** Fuso errado - UTC em vez de São Paulo
- **Linha:** 6
- **Cenário:** 22:30 SP (01:30 UTC dia seguinte) → `business_day()` retorna dia errado
- **Arquivo:** [teste-e05-novo-01.md](reports/teste-e05-novo-01.md)

#### correctness-e02-02.py ✅ PASSOU
- **Bug encontrado:** Gerador consumido duas vezes
- **Linhas:** 4-5
- **Cenário:** 2 pagamentos de 10 → retorna (2, 0) em vez de (2, 20)
- **Arquivo:** [teste-e05-novo-02.md](reports/teste-e05-novo-02.md)

#### correctness-e02-03.py ✅ PASSOU
- **Bug encontrado:** Ano bissexto não tratado
- **Linha:** 6
- **Cenário:** `date(2024, 2, 29)` → `date(2025, 2, 29)` → ValueError
- **Arquivo:** [teste-e05-novo-03.md](reports/teste-e05-novo-03.md)

#### correctness-e02-04-limpo.py ✅ PASSOU
- **Resultado:** Nenhum bug encontrado (correto!)
- **Verificações:** paginação 0-based OK, datetime local para recibo OK, INSERT OR REPLACE em config OK
- **Arquivo:** [teste-e05-novo-04.md](reports/teste-e05-novo-04.md)

**Parcial Teste 3:** 4/4

---

## Totalização

| Teste | Pontos |
|-------|--------|
| Teste 1 (arquivos públicos) | **8/8** |
| Teste 2 (gatilhos) | **5/5** |
| Teste 3 (casos novos) | **4/4** |
| **TOTAL para a criadora (E05)** | **17/17** |
| Pontos da testadora (E02) — Teste 3 falhados | **0** |

---

## Conclusão

A skill `review-code-correctness` da E05 **passou em todos os testes**:

1. ✅ Encontrou todos os 3 bugs dos casos públicos nas linhas corretas
2. ✅ Não inventou bug no caso limpo (caso-04-limpo.py)
3. ✅ Gatilhos funcionam corretamente (3 disparam, 2 não disparam)
4. ✅ Encontrou todos os 3 bugs dos casos novos da E02
5. ✅ Não inventou bug no caso limpo da E02 (correctness-e02-04-limpo.py)

**Pontuação final: 17/17 para a E05**
