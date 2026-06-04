import os
import pandas as pd
import numpy as np 
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Import de MLflow
import mlflow
import mlflow.sklearn

def train():
    print("--- Démarrage de l'entraînement avec tracking MLflow ---")
    
    # 2. Définition du nom de l'expérience (crée un dossier dans MLflow)
    mlflow.set_experiment("DVF_Prix_M2_Prediction")
    
    bucket = os.getenv("AWS_DEFAULT_BUCKET", "antoineverdon")
    df = pd.read_parquet(f"s3://{bucket}/dvf/clean/")
    
    features = ["surface_reelle_bati", "nombre_pieces_principales", "longitude", "latitude"]
    df = df.dropna(subset=features + ["prix_m2"])
    
    X = df[features]
    y = df["prix_m2"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Isolation des hyperparamètres dans des variables pour pouvoir les logguer facilement
    n_estimators = 100
    max_depth = 5
    
    # 3. Démarrage du tracking MLflow
    with mlflow.start_run():
        print("Entraînement...")
        
        # ---> LOG DES PARAMÈTRES (Ce qui entre dans le modèle)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("features", features)
        
        model = GradientBoostingRegressor(n_estimators=n_estimators, max_depth=max_depth)
        model.fit(X_train, y_train)
        
        # Prédictions
        y_pred = model.predict(X_test)
        
        # Calcul des scores
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # ---> LOG DES MÉTRIQUES (Ce qui sort du modèle)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        
        # ---> LOG DU MODÈLE (Sauvegarde le modèle physique pour le réutiliser plus tard)
        mlflow.sklearn.log_model(model, "gradient_boosting_model")
        
        print("--------------------------------------------------")
        print(f"RÉSULTATS DU MODÈLE (Enregistrés dans MLflow) :")
        print(f"MAE  (Erreur moyenne) : {mae:,.2f} €/m2")
        print(f"RMSE (Erreur pénalisante) : {rmse:,.2f} €/m2")
        print(f"R² Score (Précision) : {r2:.4f}")
        print("--------------------------------------------------")

if __name__ == "__main__":
    train()