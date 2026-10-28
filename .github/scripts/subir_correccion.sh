#!/bin/bash
# Sube sólo AGENTS.md, y sólo después de que el auditor estricto haya pasado.
# En un pull request, el commit va a esa rama. En la rutina semanal, abre un PR
# y no toca main. Un push a main no llega acá: ese evento sólo controla.

set -euo pipefail

if [ -z "${GITHUB_ACTIONS:-}" ]; then
  echo "subir_correccion.sh sólo corre en GitHub Actions." >&2
  exit 1
fi

if git diff --quiet -- AGENTS.md; then
  echo "Sin corrección mecánica."
  exit 0
fi

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

titulo="gremio: corrige un enlace roto del índice"
cuerpo="Verificado por foundry/scripts/corregir_gremio.py antes de este commit. No toca skills."

marcar_estado() {
  if [ -z "${REPO:-}" ] || [ -z "${GH_TOKEN:-}" ]; then
    return 0
  fi
  gh api "repos/${REPO}/statuses/$(git rev-parse HEAD)" \
    -f state=success \
    -f context="gremio" \
    -f description="Enlace corregido; el auditor estricto pasó en este job" \
    -f target_url="${GITHUB_SERVER_URL:-https://github.com}/${REPO}/actions/runs/${GITHUB_RUN_ID:-0}" \
    || echo "No se marcó el estado del commit."
}

if [ "${EVENT:-}" = "pull_request" ]; then
  if [ "${HEAD_REPO:-}" != "${REPO:-}" ]; then
    echo "Fork: no se sube." >&2
    exit 1
  fi
  git add -- AGENTS.md
  git commit -m "$titulo" -m "$cuerpo"
  git push origin HEAD
  marcar_estado
  exit 0
fi

rama="gremio/correccion-automatica-${GITHUB_RUN_ID:-local}"
git checkout -b "$rama"
git add -- AGENTS.md
git commit -m "$titulo" -m "$cuerpo"
git push -u origin "$rama"
marcar_estado
gh pr create --base main --head "$rama" --title "$titulo" --body "$(cat <<'EOF'
El índice de `AGENTS.md` tenía un enlace roto con un único archivo de ese nombre. Este PR cambia ese enlace.

No edita skills. `main` no cambia hasta el merge: ese es el corte.

Si más adelante el check queda rojo, el error que queda es una description, un piso o un dueño. Eso no se corrige solo.
EOF
)"
