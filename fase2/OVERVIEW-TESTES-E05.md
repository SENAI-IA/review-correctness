# Overview dos Testes da Skill E05

**Skill testada:** `review-code-correctness` (Equipe E05)  
**Equipe testadora:** E02  
**Data:** 2026-11-04  
**Repositório:** https://github.com/SENAI-IA/review-correctness

---

## Resultado Final: ✅ PASSOU EM TUDO

| Categoria | Resultado | Pontos |
|-----------|-----------|--------|
| Teste 1 - Casos Públicos | 4/4 | 8/8 |
| Teste 2 - Gatilhos | 5/5 | 5/5 |
| Teste 3 - Casos Novos E02 | 4/4 | 4/4 |
| Bônus - Caso Stress | 5/5 bugs | — |
| **TOTAL** | **100%** | **17/17** |

---

## Teste 1: Casos Públicos (8 pontos)

| Arquivo | Bug Esperado | Linha | Resultado |
|---------|--------------|-------|-----------|
| caso-01.py | Paginação errada: `page * page_size` pula primeira página | 6 | ✅ Encontrou |
| caso-02.py | `datetime.now()` devolve hora local, não UTC | 6 | ✅ Encontrou |
| caso-03.py | Webhook credita saldo em dobro no reenvio | 6-11 | ✅ Encontrou |
| caso-04-limpo.py | **Não tem bug** - skill deve dizer que está ok | — | ✅ Não inventou |

**Evidências:** `reports/teste-e05-publico-*.md`

---

## Teste 2: Gatilhos de Ativação (5 pontos)

| Prompt | Esperado | Resultado |
|--------|----------|-----------|
| "revisa a correção deste arquivo" | LIGAR | ✅ Ligou |
| "procura bugs de lógica aqui" | LIGAR | ✅ Ligou |
| "esse código está certo?" | LIGAR | ✅ Ligou |
| "explica o que essa função faz" | NÃO ligar | ✅ Não ligou |
| "revisa a segurança deste arquivo" | NÃO ligar | ✅ Não ligou |

**Evidências:** `reports/teste-e05-gatilho-*.md`

---

## Teste 3: Casos Novos da E02 (4 pontos)

| Arquivo | Bug Esperado | Linha | Resultado |
|---------|--------------|-------|-----------|
| correctness-e02-01.py | UTC vs São Paulo: data errada entre 21h-24h SP | 6 | ✅ Encontrou |
| correctness-e02-02.py | Gerador exaurido: `(2, 0)` em vez de `(2, 20)` | 4-5 | ✅ Encontrou |
| correctness-e02-03.py | Ano bissexto: `date(2025, 2, 29)` → ValueError | 6 | ✅ Encontrou |
| correctness-e02-04-limpo.py | **Não tem bug** - caso limpo proposital | — | ✅ Não inventou |

**Evidências:** `reports/teste-e05-novo-*.md`

---

## Bônus: Caso Stress (5 bugs)

Arquivo maior (~100 linhas) com múltiplos bugs de temas diferentes:

| # | Bug | Linha | Severidade | Resultado |
|---|-----|-------|------------|-----------|
| 1 | Rateio perde centavos (soma < total) | 33-37 | Crítica | ✅ |
| 2 | `timedelta` não importado → NameError | 95 | Alta | ✅ |
| 3 | `float` + `int()` trunca em taxa | 24 | Alta | ✅ |
| 4 | `datetime` naive em filtro UTC | 13-14 | Média | ✅ |
| 5 | `datetime.now()` naive vs banco UTC | 95 | Média | ✅ |

**Evidências:** `reports/teste-e05-stress.md`

---

## Estrutura dos Arquivos

```
fase2/
├── FICHA-TESTE-SKILL-E05-PREENCHIDA.md   # Ficha oficial preenchida
├── OVERVIEW-TESTES-E05.md                 # Este arquivo
├── medir.sh                               # Script de automação
├── prompts-gatilho.json                   # Prompts de teste
│
├── casos-publicos/                        # 4 casos do PDF oficial
│   ├── caso-01.py                         # Bug: paginação
│   ├── caso-02.py                         # Bug: datetime naive
│   ├── caso-03.py                         # Bug: webhook duplicado
│   └── caso-04-limpo.py                   # Limpo
│
├── casos-novos/                           # 5 casos criados pela E02
│   ├── correctness-e02-01.py              # Bug: UTC vs SP
│   ├── correctness-e02-02.py              # Bug: gerador exaurido
│   ├── correctness-e02-03.py              # Bug: ano bissexto
│   ├── correctness-e02-04-limpo.py        # Limpo
│   └── correctness-e02-stress.py          # 5 bugs (stress test)
│
└── reports/                               # Resultados dos testes
    ├── teste-e05-publico-01.md
    ├── teste-e05-publico-02.md
    ├── teste-e05-publico-03.md
    ├── teste-e05-publico-04.md
    ├── teste-e05-novo-01.md
    ├── teste-e05-novo-02.md
    ├── teste-e05-novo-03.md
    ├── teste-e05-novo-04.md
    ├── teste-e05-gatilho-1.md
    ├── teste-e05-gatilho-2.md
    ├── teste-e05-gatilho-3.md
    ├── teste-e05-gatilho-4.md
    ├── teste-e05-gatilho-5.md
    └── teste-e05-stress.md
```

---

## Conclusão

A skill `review-code-correctness` da **Equipe E05** demonstrou:

1. ✅ **Precisão:** Encontrou todos os bugs nas linhas corretas
2. ✅ **Sem falsos positivos:** Não inventou bugs nos casos limpos
3. ✅ **Gatilhos corretos:** Ativa quando deve, não ativa quando não deve
4. ✅ **Robustez:** Passou no caso stress com 5 bugs de temas variados

**Pontuação final: 17/17 (100%)**

---

*Testado por: Equipe E02*  
*Repositório skill E05: https://github.com/SENAI-IA/iapd-26t3-e05-skill-review-correctness*
