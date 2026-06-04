#!/bin/bash

echo "Création du dossier Continue..."
mkdir -p ~/.continue

echo "Génération du fichier config.yaml..."
# Les guillemets simples autour de 'EOF' sont vitaux.
# Ils disent au script d'écrire le texte "${LLM_API_KEY}" tel quel,
# sans essayer de le remplacer.
cat << 'EOF' > ~/.continue/config.yaml
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