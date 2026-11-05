<!-- skill disparou: não -->
<!-- Prompt: "explica o que essa função faz" -->
<!-- Esperado: NÃO ligar -->
<!-- Resultado: ✅ PASSOU - skill NÃO ativou (correto) -->

A skill `review-code-correctness` da E05 NÃO DEVE disparar com este prompt porque:
- A description diz claramente no fim: "Não use para revisar specs, nem para estilo, performance ou segurança"
- "Explica o que faz" é pedido de explicação, não de revisão de correção
- Não menciona bug, erro, correção ou lógica
