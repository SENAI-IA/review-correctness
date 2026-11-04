#!/usr/bin/env bash
# Mede a skill da adversária como manda a ficha-teste: sessão nova por caso, 1ª resposta vale.
# Uso: bash medir.sh <pasta-da-skill-da-adversaria> <nome-da-equipe>
set -u
SKILL="$(realpath "$1")"; EQ="$2"; AQUI="$(cd "$(dirname "$0")" && pwd)"
W="$(mktemp -d)"; mkdir -p "$W/.claude/skills" "$AQUI/reports"
cp -r "$SKILL" "$W/.claude/skills/"
cp "$AQUI"/casos-publicos/*.py "$AQUI"/casos-novos/*.py "$W/"
cd "$W" && git init -q
roda(){ timeout 280 claude -p "$2" ${MODELO:+--model $MODELO} --output-format stream-json --verbose \
  --allowedTools "Read,Bash(python3:*),Bash(python:*),Skill,Glob,Grep" > "$W/$1.jsonl" 2>/dev/null; }
i=0; for c in caso-01 caso-02 caso-03 caso-04-limpo; do i=$((i+1))
  roda "publico-0$i" "revisa a correção deste arquivo: $c.py" & done
i=0; for c in correctness-e02-01 correctness-e02-02 correctness-e02-03 correctness-e02-04-limpo; do i=$((i+1))
  roda "novo-0$i" "revisa a correção deste arquivo: $c.py" & done
n=0; while IFS= read -r p; do n=$((n+1)); roda "gatilho-$n" "$p" & done \
  < <(python3 -c "import json;[print(x['prompt']) for x in json.load(open('$AQUI/prompts-gatilho.json'))]")
wait
for f in "$W"/*.jsonl; do b=$(basename "$f" .jsonl)
  python3 - "$f" "$AQUI/reports/correctness-$EQ-$b.md" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
skill, res = False, ""
for l in open(src):
    try: d = json.loads(l)
    except ValueError: continue
    if '"name": "Skill"' in json.dumps(d) or '"name":"Skill"' in l: skill = True
    if d.get("type") == "result": res = d.get("result", "")
open(dst, "w").write(f"<!-- skill disparou: {'sim' if skill else 'não'} -->\n{res}\n")
print(f"{dst.rsplit('/',1)[1]:45s} skill={'sim' if skill else 'não'}")
PY
done
echo "Saídas em $AQUI/reports/. Preencha a ficha-teste.md a partir delas."
