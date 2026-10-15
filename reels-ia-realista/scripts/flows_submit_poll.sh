#!/usr/bin/env bash
# Uso: bash scripts/flows_submit_poll.sh <image|video> <body.json> <arquivo_saida_sem_extensao>
# Envia POST /v1/flows/<tipo>, faz polling com backoff (vídeo: 10 s dobrando até 60 s, teto 30 min; imagem: 2 s, teto 5 min)
# e baixa o content_url com a extensão do content_mime_type. Equivalente em Python: scripts/el.py submit + wait.
# ATENÇÃO: o POST gasta créditos se for aceito. Não imprime a chave. Precisa de curl e jq.
# Saída: 0 ok | 1 create recusado (nada cobrado) | 2 geração falhou (não cobrada) | 3 timeout local (consulte depois pelo id).
set -euo pipefail
KIND="$1"; BODY="$2"; OUTBASE="$3"
if [ -z "${ELEVENLABS_API_KEY:-}" ]; then
  set -a; source "${ELEVENLABS_ENV_FILE:-$HOME/.config/elevenlabs/env}"; set +a
fi
API=https://api.elevenlabs.io/v1/flows/$KIND
RESP=$(curl -sS -X POST "$API" -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" --data-binary @"$BODY")
ID=$(jq -r '.id // empty' <<<"$RESP")
if [ -z "$ID" ]; then echo "create rejeitado (nada cobrado): $RESP" >&2; exit 1; fi
echo "generation_id=$ID"
if [ "$KIND" = video ]; then DELAY=10; MAXWAIT=1800; else DELAY=2; MAXWAIT=300; fi
WAITED=0
while :; do
  R=$(curl -sS "$API/$ID" -H "xi-api-key: $ELEVENLABS_API_KEY")
  case "$(jq -r .status <<<"$R" 2>/dev/null)" in
    completed)
      MIME=$(jq -r .content_mime_type <<<"$R"); EXT=${MIME##*/}; [ "$EXT" = jpeg ] && EXT=jpg
      mkdir -p "$(dirname "$OUTBASE")"
      curl -sSL "$(jq -r .content_url <<<"$R")" -o "$OUTBASE.$EXT"
      echo "ok: $OUTBASE.$EXT ($MIME)"; break ;;
    failed)
      jq '{id,failure_reason,error_message}' <<<"$R" >&2; exit 2 ;;
  esac
  [ "$WAITED" -ge "$MAXWAIT" ] && { echo "timeout local após ${WAITED}s; id=$ID (consulte depois com GET $API/$ID)" >&2; exit 3; }
  sleep "$DELAY"; WAITED=$((WAITED+DELAY))
  if [ "$KIND" = video ]; then DELAY=$(( DELAY*2 > 60 ? 60 : DELAY*2 )); fi
done
