import os
import pandas as pd
import numpy as np 
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train():
    print("--- Démarrage de l'entraînement avec évaluation complète ---")
    
    bucket = os.getenv("AWS_DEFAULT_BUCKET", "antoineverdon")
    df = pd.read_parquet(f"s3://{bucket}/dvf/clean/")
    
    features = ["surface_reelle_bati", "nombre_pieces_principales", "longitude", "latitude"]
    df = df.dropna(subset=features + ["prix_m2"])
    
    X = df[features]
    y = df["prix_m2"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Entraînement...")
    model = GradientBoostingRegressor(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)
    
    # Prédictions
    y_pred = model.predict(X_test)
    
    # Calcul des scores
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print("--------------------------------------------------")
    print(f"RÉSULTATS DU MODÈLE :")
    print(f"MAE  (Erreur moyenne) : {mae:,.2f} €/m2")
    print(f"RMSE (Erreur pénalisante) : {rmse:,.2f} €/m2")
    print(f"R² Score (Précision) : {r2:.4f}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    train()