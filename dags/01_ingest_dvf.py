from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable # <-- Nouvel import Airflow
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

def ingest():
    # Ingestion des données de Paris (75) pour le POC
    url = "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/75.csv.gz"
    df = pd.read_csv(url, compression="gzip", low_memory=False)
    
    # Récupération sécurisée via le coffre-fort interne d'Airflow
    db_user = Variable.get("POSTGRES_SECRETS_USERNAME")
    db_password = Variable.get("POSTGRES_SECRETS_PASSWORD")
    db_host = Variable.get("POSTGRES_SECRETS_HOST")
    db_name = Variable.get("POSTGRES_SECRETS_NAME")
      
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    engine = create_engine(connection_string)
    
    df.to_sql("dvf_raw", engine, if_exists="replace", index=False)
    print(f"Ingestion réussie : {len(df)} lignes ajoutées dans postgres.")

with DAG("01_ingest_dvf", start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False) as dag:
    PythonOperator(task_id="ingest_to_postgres", python_callable=ingest)