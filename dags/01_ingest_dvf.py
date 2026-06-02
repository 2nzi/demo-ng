from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import os

def ingest():
    # Ingestion des données de Paris (75) pour le POC
    url = "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/75.csv.gz"
    df = pd.read_csv(url, compression="gzip", low_memory=False)
    
    # Récupération sécurisée des accès via les variables d'environnement (avec fallback)
    db_user = os.getenv("POSTGRES_SECRETS_USERNAME", "postgres")
    db_password = os.getenv("POSTGRES_SECRETS_PASSWORD", "postgres")
    db_host = os.getenv("POSTGRES_SECRETS_HOST", "postgresql-dvf-postgresql")
    db_name = "postgres"
    
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    engine = create_engine(connection_string)
    
    df.to_sql("dvf_raw", engine, if_exists="replace", index=False)
    print(f"Ingestion réussie : {len(df)} lignes ajoutées dans postgres.")

with DAG("01_ingest_dvf", start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False) as dag:
    PythonOperator(task_id="ingest_to_postgres", python_callable=ingest)