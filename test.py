import os
import boto3
import pandas as pd
from io import StringIO

# Récupère l'URL de l'endpoint S3
endpoint_url = "https://" + os.environ.get("AWS_S3_ENDPOINT")

# Crée une session boto3
session = boto3.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_REGION")
)

# Crée un client S3
s3_client = session.client('s3', endpoint_url=endpoint_url)

# Le bucket et le chemin de ton fichier sur S3
bucket_name = "antoineverdon"
file_key = "test_onyxia.csv"

# Télécharge le fichier depuis S3
response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
data = response['Body'].read().decode('utf-8')

# Utilise pandas pour lire le fichier CSV à partir de la chaîne de caractères
df = pd.read_csv(StringIO(data))

# Affiche le DataFrame
print(df)