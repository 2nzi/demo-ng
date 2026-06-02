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
    
    # Utilisation du DNS interne Kubernetes fourni par Onyxia pour Postgres
    # Remplace 'postgresql-dvf' par le nom exact de ton service s'il est différent
    engine = create_engine("postgresql://postgres:postgres@postgresql-dvf-postgresql:5432/postgres")
    df.to_sql("dvf_raw", engine, if_exists="replace", index=False)
    print(f"Ingestion réussie : {len(df)} lignes ajoutées dans postgres.")

with DAG("01_ingest_dvf", start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False) as dag:
    PythonOperator(task_id="ingest_to_postgres", python_callable=ingest)