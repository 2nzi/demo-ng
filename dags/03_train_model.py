from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def train():
    import mlflow
    import pandas as pd
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error
    
    # Connexion au serveur MLflow interne Onyxia
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("demo-ng-immobilier")
    
    bucket = os.getenv("AWS_DEFAULT_BUCKET")
    # Lecture directe du Parquet sur S3 via pandas/pyarrow
    df = pd.read_parquet(f"s3://{bucket}/dvf/clean/")
    
    features = ["surface_reelle_bati", "nombre_pieces_principales", "longitude", "latitude"]
    df = df.dropna(subset=features + ["prix_m2"])
    
    X = df[features]
    y = df["prix_m2"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    with mlflow.start_run():
        model = GradientBoostingRegressor(n_estimators=100, max_depth=5)
        model.fit(X_train, y_train)
        
        mae = mean_absolute_error(y_test, model.predict(X_test))
        
        # Logging des métriques et sauvegarde du modèle
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(model, "model_immobilier")
        print(f"Modèle entraîné avec succès. MAE: {mae}")

with DAG("03_train_model", start_date=datetime(2026, 1, 1), schedule="@weekly", catchup=False) as dag:
    PythonOperator(task_id="train_and_log_mlflow", python_callable=train)