# Resultados da Skill E05 — `review-code-correctness`

Avaliação da skill de revisão de correção da Equipe 05 usando Kiro.
Data: 2026-11-04

## Resumo

| Categoria | Total | Skill disparou | Acertos |
|-----------|-------|----------------|---------|
| Casos públicos | 4 | 4/4 | — |
| Casos novos | 4 | 4/4 | — |
| Gatilhos (dispara) | 3 | 3/3 | 3/3 ✅ |
| Gatilhos (não-dispara) | 2 | 0/2 | 2/2 ✅ |
| **Total gatilhos** | **5** | — | **5/5 ✅** |

## Casos Públicos

| Teste | Arquivo | Bugs esperados | Bugs encontrados | Relatório |
|-------|---------|----------------|------------------|-----------|
| publico-01 | `caso-01.py` | 1 (off-by-one) | 1 alta ✅ | [correctness-e05-kiro-publico-01.md](correctness-e05-kiro-publico-01.md) |
| publico-02 | `caso-02.py` | 1 (datetime naive) | 3 (2 altas, 1 média) ✅ | [correctness-e05-kiro-publico-02.md](correctness-e05-kiro-publico-02.md) |
| publico-03 | `caso-03.py` | 1 (idempotência webhook) | 1 alta ✅ | [correctness-e05-kiro-publico-03.md](correctness-e05-kiro-publico-03.md) |
| publico-04 | `caso-04-limpo.py` | 0 (código limpo) | 2 médias (race condition) | [correctness-e05-kiro-publico-04.md](correctness-e05-kiro-publico-04.md) |

## Casos Novos (criados pela E02)

| Teste | Arquivo | Bugs esperados | Bugs encontrados | Relatório |
|-------|---------|----------------|------------------|-----------|
| novo-01 | `correctness-e02-01.py` | 1 (UTC vs São Paulo) | 3 (2 altas, 1 média) ✅ | [correctness-e05-kiro-novo-01.md](correctness-e05-kiro-novo-01.md) |
| novo-02 | `correctness-e02-02.py` | 1 (gerador exaurido) | 1 alta ✅ | [correctness-e05-kiro-novo-02.md](correctness-e05-kiro-novo-02.md) |
| novo-03 | `correctness-e02-03.py` | 1 (ano bissexto) | 1 alta ✅ | [correctness-e05-kiro-novo-03.md](correctness-e05-kiro-novo-03.md) |
| novo-04 | `correctness-e02-04-limpo.py` | 0 (código limpo) | 0 ✅ | [correctness-e05-kiro-novo-04.md](correctness-e05-kiro-novo-04.md) |

## Gatilhos de Ativação

| Teste | Prompt | Esperado | Obtido | Status |
|-------|--------|----------|--------|--------|
| gatilho-1 | "o summarize está devolvendo total zero, tem bug aí?" | dispara | dispara | ✅ |
| gatilho-2 | "esse código está certo?" | dispara | dispara | ✅ |
| gatilho-3 | "antes do merge, confere se a lógica funciona em todos os casos" | dispara | dispara | ✅ |
| gatilho-4 | "explica o que essa função faz" | não-dispara | não-dispara | ✅ |
| gatilho-5 | "está protegida contra SQL injection?" | não-dispara | não-dispara | ✅ |

## Avaliação Qualitativa

### Pontos fortes da skill E05:
- ✅ Boa cobertura das 5 lentes (lógica, borda, erro, estado, data/fuso)
- ✅ Gotchas detalhados (datetime naive, idempotência, arredondamento)
- ✅ Formato de resposta padronizado e consistente
- ✅ Checklist rápido útil
- ✅ Gatilhos funcionam corretamente (5/5)

### Observações:
- O caso `publico-04` (limpo) encontrou 2 bugs de média severidade que são discutíveis (race condition em webhook e validação de page). São achados válidos, mas podem ser considerados over-reporting dependendo do contrato.
- O caso `novo-04` (limpo) foi corretamente identificado como sem bugs.

## Arquivos gerados

```
reports/
├── correctness-e05-kiro-publico-01.md
├── correctness-e05-kiro-publico-02.md
├── correctness-e05-kiro-publico-03.md
├── correctness-e05-kiro-publico-04.md
├── correctness-e05-kiro-novo-01.md
├── correctness-e05-kiro-novo-02.md
├── correctness-e05-kiro-novo-03.md
├── correctness-e05-kiro-novo-04.md
├── correctness-e05-kiro-gatilho-1.md
├── correctness-e05-kiro-gatilho-2.md
├── correctness-e05-kiro-gatilho-3.md
├── correctness-e05-kiro-gatilho-4.md
└── correctness-e05-kiro-gatilho-5.md
```
