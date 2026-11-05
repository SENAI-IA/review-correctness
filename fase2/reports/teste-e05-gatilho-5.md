<!-- skill disparou: não -->
<!-- Prompt: "revisa a segurança deste arquivo" -->
<!-- Esperado: NÃO ligar -->
<!-- Resultado: ✅ PASSOU - skill NÃO ativou (correto) -->

A skill `review-code-correctness` da E05 NÃO DEVE disparar com este prompt porque:
- A description diz explicitamente no fim: "Não use para revisar specs, nem para estilo, performance ou segurança"
- "Revisa a segurança" é outro tema, não correção de lógica
