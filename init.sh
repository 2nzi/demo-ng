#!/bin/bash
set -e

echo "➡️ Installation extensions UI / Data viz"

# === CSV visuel (gros impact pour ton screen) ===
code-server --install-extension mechatroner.rainbow-csv

# === amélioration UX globale ===
code-server --install-extension naumovs.color-highlight
code-server --install-extension usernamehw.errorlens

# === thème (important pour le rendu visuel) ===
code-server --install-extension dracula-theme.theme-dracula

echo "➡️ Configuration VS Code"

mkdir -p ~/.local/share/code-server/User

cat <<EOF > ~/.local/share/code-server/User/settings.json
{
  // ===== THEME =====
  "workbench.colorTheme": "Dracula",

  // ===== CSV (effet visuel principal) =====
  "files.associations": {
    "*.csv": "csv"
  },

  "rainbow_csv.separator": ";",
  "rainbow_csv.autodetect_separators": [",", ";", "\\t"],
  "rainbow_csv.enable_auto_csv_lint": true,
  "rainbow_csv.highlight_rows": true,

  // ===== Python (cohérent avec ton setup actuel) =====
  "python.analysis.typeCheckingMode": "basic",
  "editor.formatOnSave": true,

  // Ruff déjà installé chez toi → on l’active proprement
  "ruff.enable": true,

  // ===== UI lisibilité =====
  "editor.minimap.enabled": false,
  "editor.renderWhitespace": "all",
  "editor.cursorSmoothCaretAnimation": true,

  // ===== Jupyter (déjà présent dans ton env) =====
  "jupyter.askForKernelRestart": false,

  // ===== CSV/texte =====
  "[csv]": {
    "editor.wordWrap": "off",
    "editor.quickSuggestions": false
  }
}
EOF

echo "✅ VS Code configuré (UI + CSV + theme)"