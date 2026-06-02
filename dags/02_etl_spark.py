from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def etl_spark():
    from pyspark.sql import SparkSession
    
    # Configuration de Spark pour inclure les connecteurs S3 et Postgres
    spark = (SparkSession.builder
             .appName("dvf-etl-spark")
             .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3,org.apache.hadoop:hadoop-aws:3.3.4")
             .getOrCreate())
    
    # Lecture depuis PostgreSQL
    df = (spark.read.format("jdbc")
          .option("url", "jdbc:postgresql://postgresql-dvf-postgresql:5432/postgres")
          .option("dbtable", "dvf_raw")
          .option("user", "postgres").option("password", "postgres")
          .load())
    
    # Nettoyage et calcul du prix au m²
    df_clean = (df.filter("valeur_fonciere IS NOT NULL")
                  .filter("surface_reelle_bati > 0")
                  .withColumn("prix_m2", df.valeur_fonciere / df.surface_reelle_bati))
    
    # Écritures des parquets nettoyés sur le stockage S3 (MinIO)
    bucket = os.getenv("AWS_DEFAULT_BUCKET", "mon-bucket-defaut")
    df_clean.write.mode("overwrite").parquet(f"s3a://{bucket}/dvf/clean/")
    spark.stop()

with DAG("02_etl_spark", start_date=datetime(2026, 1, 1), schedule="@daily", catchup=False) as dag:
    PythonOperator(task_id="run_pyspark_clean", python_callable=etl_spark)