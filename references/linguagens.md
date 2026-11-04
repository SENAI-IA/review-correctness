# Armadilhas de correção por linguagem

Leia só a seção da linguagem do arquivo revisado.

## Python
- `datetime.now()` / `utcnow()` / `date.today()` → naive (sem fuso); usar `datetime.now(timezone.utc)` ou `ZoneInfo`
- Argumento default mutável: `def f(x=[])` → compartilhado entre chamadas
- `round(2.5) == 2` (arredondamento bancário); `int(19.99 * 100) == 1998`
- `is` com número/string compara identidade, não valor

## JavaScript / TypeScript
- `new Date().getMonth()` vai de 0 a 11
- `new Date("2026-11-04")` é interpretado como UTC; `new Date("2026-11-04T00:00")` como horário local
- `arr.sort()` sem comparador ordena como string: [10, 9, 1] → [1, 10, 9]
- `==` com coerção; `0 || padrao` descarta o zero (use `??`)
- `0.1 + 0.2 !== 0.3`: dinheiro em centavos inteiros
- `forEach` com `async` não espera; `return` dentro de `forEach` não sai da função

## Java
- `LocalDateTime` não tem fuso; para instantes, use `Instant` ou `ZonedDateTime`
- `Integer` comparado com `==` fora da faixa -128..127 dá false (use `equals`)
- `String` comparada com `==` compara referência
- `double` para dinheiro: use `BigDecimal` (construído a partir de String)

## SQL
- `BETWEEN` em timestamp inclui o limite superior, mas `BETWEEN '...-01' AND '...-31'` perde o último dia depois de 00:00 (use `>= início AND < próximo dia`)
- `NOT IN` com subquery que retorna NULL → nenhuma linha
- `= NULL` nunca é verdadeiro (use `IS NULL`)
- `LIMIT/OFFSET` sem `ORDER BY` não tem ordem garantida
