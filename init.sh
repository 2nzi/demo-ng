#!/bin/bash

echo "Création du dossier Continue..."
mkdir -p ~/.continue

echo "Génération du fichier config.yaml..."
# ATTENTION : Il n'y a plus de guillemets autour de EOF !
# Bash va prendre la valeur de ton Vault et l'écrire en dur dans le fichier.
cat << EOF > ~/.continue/config.yaml
name: SSPCloud Config
version: 1.0.0
schema: v1

models:
  - name: qwen3-6-35b-moe
    provider: openai
    model: qwen3-6-35b-moe
    apiKey: ${LLM_API_KEY}
    apiBase: https://llm.lab.sspcloud.fr/api
EOF

echo "Configuration Continue terminée !"