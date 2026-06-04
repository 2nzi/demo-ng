#!/bin/bash

echo "Configuration du thème VS Code en mode clair..."

# Définition du dossier où VS Code stocke ses paramètres
VSCODE_SETTINGS_DIR="$HOME/.local/share/code-server/User"

# Création du dossier s'il n'existe pas déjà
mkdir -p "$VSCODE_SETTINGS_DIR"

# Injection du paramètre de thème clair dans le fichier settings.json
cat << 'EOF' > "$VSCODE_SETTINGS_DIR/settings.json"
{
    "workbench.colorTheme": "Default Light+"
}
EOF

echo "✅ Thème clair configuré avec succès !"