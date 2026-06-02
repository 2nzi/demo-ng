from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime
import os

def etl_spark():
    from pyspark.sql import SparkSession
    
    # 1. Rendre le bucket dynamique via une Variable Airflow
    bucket = Variable.get("s3_bucket_name", default_var="antoineverdon")
    
    # 2. Récupération des secrets d'infrastructure injectés par Onyxia
    s3_endpoint = os.environ.get("AWS_S3_ENDPOINT")
    s3_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    s3_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    s3_session_token = os.environ.get("AWS_SESSION_TOKEN")
    
    # 3. Récupération des secrets de la base de données injectés par Vault
    db_user = os.getenv("POSTGRES_SECRETS_USERNAME", "postgres")
    db_password = os.getenv("POSTGRES_SECRETS_PASSWORD", "postgres")
    db_host = os.getenv("POSTGRES_SECRETS_HOST", "postgresql-dvf-postgresql")
    db_name = os.getenv("POSTGRES_SECRETS_NAME", "defaultdb") # Prise en compte du nom dynamique  
    jdbc_url = f"jdbc:postgresql://{db_host}:5432/{db_name}"

    # 4. Configuration de la session Spark
    spark = (SparkSession.builder
             .appName("dvf-etl-spark")
             .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3,org.apache.hadoop:hadoop-aws:3.3.4")
             .config("spark.hadoop.fs.s3a.endpoint", s3_endpoint)
             .config("spark.hadoop.fs.s3a.access.key", s3_access_key)
             .config("spark.hadoop.fs.s3a.secret.key", s3_secret_key)
             .config("spark.hadoop.fs.s3a.session.token", s3_session_token)
             .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider")
             .config("spark.hadoop.fs.s3a.path.style.access", "true")
             .getOrCreate())
    
    # Execution du traitement
    df = spark.read.format("jdbc").option("url", jdbc_url).option("dbtable", "dvf_raw").option("user", db_user).option("password", db_password).load()
    df_clean = df.filter("valeur_fonciere IS NOT NULL").filter("surface_reelle_bati > 0").withColumn("prix_m2", df.valeur_fonciere / df.surface_reelle_bati)
    
    # Écriture dynamique
    df_clean.write.mode("overwrite").parquet(f"s3a://{bucket}/dvf/clean/")
    spark.stop()

with DAG("02_etl_spark", start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False) as dag:
    PythonOperator(task_id="run_pyspark_clean", python_callable=etl_spark)