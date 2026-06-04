import os
import pandas as pd

# On récupère l'URL du S3
endpoint_url = "https://" + os.environ.get("AWS_S3_ENDPOINT")

# Le chemin de votre fichier sur S3
chemin_s3 = "s3://antoineverdon/test_onyxia.csv"

# Lecture directe du fichier depuis le cloud
df = pd.read_csv(
    chemin_s3,
    storage_options={
        "client_kwargs": {"endpoint_url": endpoint_url}
    }
)

print(df)