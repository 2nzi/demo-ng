import os
from pyspark.sql import SparkSession
# Import des fonctions SQL pour manipuler les colonnes de manière robuste
from pyspark.sql.functions import col 

def etl_spark():
    print("Démarrage de la session Spark...")
    
    # 1. Bucket S3 configuré en dur pour ton environnement VSCode
    bucket = "antoineverdon"
    
    # 2. Récupération des secrets d'infrastructure injectés par Onyxia
    s3_endpoint = os.environ.get("AWS_S3_ENDPOINT")
    s3_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    s3_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    s3_session_token = os.environ.get("AWS_SESSION_TOKEN")
    
    # 3. Récupération des secrets de la base de données
    db_user = os.environ["POSTGRES_SECRETS_USERNAME"]
    db_password = os.environ["POSTGRES_SECRETS_PASSWORD"]
    db_host = os.environ["POSTGRES_SECRETS_HOST"]
    db_name = os.environ["POSTGRES_SECRETS_NAME"]
    jdbc_url = f"jdbc:postgresql://{db_host}:5432/{db_name}"

    # 4. Configuration de la session Spark avec les drivers nécessaires
    spark = (SparkSession.builder
             .appName("dvf-etl-spark-local")
             .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3,org.apache.hadoop:hadoop-aws:3.3.4")
             .config("spark.hadoop.fs.s3a.endpoint", s3_endpoint)
             .config("spark.hadoop.fs.s3a.access.key", s3_access_key)
             .config("spark.hadoop.fs.s3a.secret.key", s3_secret_key)
             .config("spark.hadoop.fs.s3a.session.token", s3_session_token)
             .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider")
             .config("spark.hadoop.fs.s3a.path.style.access", "true")
             .getOrCreate())
    
    print("Lecture depuis Postgres...")
    # Lecture des données brutes
    df = (spark.read
          .format("jdbc")
          .option("url", jdbc_url)
          .option("dbtable", "dvf_raw")
          .option("user", db_user)
          .option("password", db_password)
          .option("driver", "org.postgresql.Driver")
          .load())
    
    print("Nettoyage des données...")
    # Transformation : filtrage et calcul du prix au m² avec les fonctions SQL
    df_clean = df.filter(col("valeur_fonciere").isNotNull()) \
                 .filter(col("surface_reelle_bati") > 0) \
                 .withColumn("prix_m2", col("valeur_fonciere") / col("surface_reelle_bati"))
    
    print("Écriture dans S3 au format Parquet...")
    # Écriture du résultat final
    df_clean.write.mode("overwrite").parquet(f"s3a://{bucket}/dvf/clean/")
    
    spark.stop()
    print("ETL terminé avec succès !")

if __name__ == "__main__":
    etl_spark()