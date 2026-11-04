---
name: review-correctness
description: >
  Revisão de correção de código. Use SEMPRE que pedirem "revisa a correção deste
  arquivo", "procura bugs de lógica aqui", "esse código está certo?", "tem bug aqui?",
  "procura o bug", "está quebrando/dando errado", "funciona em todos os casos?" ou
  review de lógica antes de merge: qualquer pedido para julgar se um código está certo
  ou achar bug/erro, mesmo pergunta curta sobre um arquivo ou uma função só.
  Cobre lógica, borda (off-by-one, paginação, vazio, zero, negativo, virada de mês/ano,
  arredondamento e rateio), estado (idempotência, reenvio, efeito duplicado, transição
  de status) e data/fuso (datetime naive, hora local no lugar de UTC), em Python,
  JS/TS, Java ou SQL. Devolve achados com arquivo, linha, severidade e evidência. Não
  cobre segurança (injeção, auth, segredo, log sensível) nem desempenho (lentidão,
  N+1, complexidade, índice); não escreve testes, não corrige nem refatora código e
  não explica o que um diff faz.
license: Apache-2.0
compatibility: Requer python3 para os scripts (o review vale para qualquer linguagem).
metadata:
  author: IAPD-26T3-E02
  version: "2.2"
---

# review-correctness

O código faz o que promete? Reporte só o que produz **resultado errado** com alguma
entrada, horário ou sequência de eventos. Cada achado sai com arquivo, linha e
evidência; sem linha, o achado não existe. Não suponha nada além do que está no arquivo.

## Quando NÃO usar

- "Escreve o teste do webhook/reembolso": é escrever teste, não review.
- "Revisa a segurança" / "tem falha de injeção?" / "o token está seguro?": `review-security`.
- "Revisa o desempenho" / "essa query está lenta?": `review-performance`.
- "Explica o que esse diff faz", "corrige esse bug", "refatora isso": não é procurar bugs.

## Gotchas (onde o modelo erra sem esta skill)

Borda e off-by-one
- Paginação 1-based (`page=1` são os primeiros): `offset = page * size` pula a
  primeira página; o certo é `(page - 1) * size`. A docstring/comentário diz se é
  0- ou 1-based; o bug é o código contradizer o contrato.
- Laço que acessa `i+1` e para um antes do fim está **correto**; não é off-by-one.
- Limites: `<` contra `<=` (expira "após 30 dias", "até 10 itens"), intervalo de datas
  com fim inclusivo/exclusivo trocado, `range(1, n)` que perde o último, último item
  ou `max()` em lista vazia, divisão por zero.
- Entrada não validada: valor negativo, zero, nulo ou tipo errado aceitos onde a
  regra pede positivo.

Dinheiro e números
- Quantia em ponto flutuante, `round()` em float, truncamento (`int(19.99*100)` = 1998)
  ou divisão gerando fração em centavos: valor errado. Use inteiro em centavos ou
  decimal; rateio precisa distribuir o resto (soma das partes = total).
- Saldo que fica negativo sem checar fundos; estorno cuja soma excede o valor original.

Data e fuso
- Python: `datetime.now()`, `datetime.utcnow()`, `date.today()`, `fromtimestamp(x)` e
  `strptime` devolvem datetime **naive** (sem tzinfo). Se nome, docstring ou coluna diz
  **UTC**, é bug: use `datetime.now(timezone.utc)`. Naive em hora local quebra na troca
  de fuso/horário de verão; naive menos aware levanta `TypeError`.
- `.replace(tzinfo=...)` reinterpreta o relógio (não converte); converter é
  `.astimezone(...)`. Outras linguagens: `references/linguagens.md`.

Estado e idempotência
- Evento que pode chegar de novo (webhook, fila, retry, job, clique duplo) deve ter
  efeito uma vez só. `INSERT OR REPLACE`, `REPLACE INTO` e upsert **não** deduplicam:
  sobrescrevem o registro e deixam o efeito (crédito, e-mail, baixa) rodar de novo.
- Checar o ID antes do efeito (`SELECT` → `return` se já existe → `INSERT` + efeito no
  mesmo commit) **está correto** para reenvio. Também correto: `INSERT OR IGNORE` /
  `ON CONFLICT DO NOTHING` checando se inseriu antes do efeito.
- Efeito colateral antes da checagem de duplicata, ou gravação parcial sem
  `commit`/`rollback` coerente: estado fica pela metade.
- Transição de status sem validar o estado atual (reembolsar `pending`, pagar duas vezes).
- Estado compartilhado entre chamadas: argumento padrão mutável (`def f(x=[])`),
  alterar lista/dict enquanto itera, cópia rasa onde precisava cópia.

Lógica e retorno
- Condição invertida, `and`/`or` trocados, `return` antecipado que pula um caso,
  `is` comparando número/string, variável sobrescrita no laço.
- Falha sinalizada com `None`, `-1`, `False` ou erro engolido (`except: pass`,
  `catch {}`): o chamador segue como se tivesse dado certo.
- Entidade inexistente devolvendo valor "normal" (saldo 0, lista vazia) em vez de erro.

Disciplina contra falso positivo (caso limpo)
- Antes de reportar, escreva a **entrada concreta que quebra o código** e o resultado
  obtido vs esperado. Se não conseguir, não reporte.
- Achado que depende do que você **não vê** (schema, unicidade de coluna, outro arquivo,
  "se X puder repetir") não entra na tabela: vira nota `baixo` no fim. Ex.:
  `ORDER BY created_at` sem desempate é nota baixo, não achado.
- Falha hipotética de infraestrutura (banco travado, exceção do driver, rede, disco,
  "e se o UPDATE levantar exceção?") não é bug de correção: no máximo nota `baixo`.
  Achado precisa de uma entrada **válida** que dá resultado errado sem nada falhar.
- Corrida entre requisições **simultâneas** (lock, atomicidade entre workers),
  segurança e desempenho são outros temas: no máximo nota `baixo`, nunca médio ou maior.
- Estilo, nomes, tipos, docstring, "poderia validar mais" sem regra violada: não é bug.

## Procedimento

1. Rode `python3 scripts/numerar.py <arquivo>` (caminho relativo a esta skill) e leia o
   arquivo **numerado**. Toda linha citada sai desta numeração; nunca conte de cabeça.
2. Se for Python, rode `python3 scripts/sinais.py <arquivo-ou-pasta>`: lista linhas
   suspeitas por regex. Cada sinal é **pista a confirmar**, não achado.
3. Identifique a linguagem; se não for Python, consulte `references/linguagens.md`.
4. Para cada função, anote o que nome/docstring/comentário **promete** e passe pelos
   gotchas: borda → dinheiro → data/fuso → estado → lógica. Teste mentalmente com vazio,
   1 elemento, o último, o limite exato, reenvio do mesmo ID e 23h59 no fuso -03.
5. Para cada bug: arquivo, linha (ou `6-11`), regra, severidade, trecho de código +
   entrada que quebra (obtido vs esperado) como evidência, e a correção em uma frase.
6. Releia aplicando a "Disciplina contra falso positivo" e entregue no template.

## Severidade

| Severidade | Quando |
|---|---|
| crítico | dinheiro/saldo errado ou duplicado, dado corrompido ou perdido |
| alto | resultado errado no caminho normal (página pulada, efeito repetido em reenvio) |
| médio | erro em borda, em troca de fuso ou falha sinalizada com `None` |
| baixo | risco teórico, fora do tema ou sem caminho de execução claro |

## Template de saída (obrigatório)

```
## Review de correção: <arquivo>

| # | Arquivo | Linha | Requisito | Severidade | Evidência | Sugestão |
|---|---|---|---|---|---|---|
| 1 | caso-01.py | 6 | paginação 1-based | alto | `offset = page * page_size`: com page=1 o offset é 20; obtido registros 21-40, esperado 1-20 | `offset = (page - 1) * page_size` |
```

- `Requisito`: o requisito da spec do projeto, se houver (ex.: `R11`); senão a regra
  violada em poucas palavras (`idempotência`, `UTC`, `off-by-one`).
- Sem bug: escreva `Nenhum achado de correção.` (sem tabela) e, em 1 linha, as bordas
  verificadas.
- Notas de outros temas, se houver, vão depois em `Fora do tema (baixo):`.

## Validation loop

1. `python validate.py <esta pasta>` passa (frontmatter).
2. Os 5 prompts de `evals/evals.json` em sessão nova: 3 disparam, 2 não.
3. Nos casos de `evals/evals.json`, acha o bug na linha certa e fica em silêncio no
   caso limpo. O que deixar passar vira gotcha novo aqui.
