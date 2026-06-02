#!/bin/sh
# Script d'initialisation pour le projet demo-ng
echo "=== Installation des dépendances Python ==="
pip install --quiet pandas scikit-learn mlflow psycopg2-binary sqlalchemy pyarrow s3fs

# echo "=== Vérification de l'accès S3 ==="
# if [ -n "$AWS_DEFAULT_BUCKET" ]; then
#     echo "Espace de stockage S3 détecté : $AWS_DEFAULT_BUCKET"
# else
#     echo "Attention : Aucun bucket S3 configuré."
# fi
echo "=== Environnement prêt ==="