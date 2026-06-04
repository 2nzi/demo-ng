import os
import requests

def call_llm():
    # 1. On récupère la clé, SANS valeur par défaut codée en dur
    api_key = os.getenv("LLM_API_KEY") 
    
    # Sécurité : on bloque le script si la clé n'est pas trouvée dans l'environnement
    if not api_key:
        raise ValueError("Erreur : La variable d'environnement LLM_API_KEY n'est pas définie. Pense à faire 'export LLM_API_KEY=...' dans ton terminal.")

    url = "https://llm.lab.sspcloud.fr/api/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        # 2. Correction du modèle ("moe" au lieu de "one")
        "model": "qwen3-6-35b-moe",
        "messages": [
            {"role": "user", "content": "Bonjour, donne-moi le top 10 de micros spécifique hélicoptère."}
        ]
    }

    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status() # Lève une erreur si le code HTTP n'est pas 200
        
        data = resp.json()
        print("Réponse du LLM :\n")
        print(data['choices'][0]['message']['content'])
        
    except requests.exceptions.HTTPError as http_err:
        print(f"Erreur HTTP : {http_err}")
        # Affiche le message d'erreur précis renvoyé par SSPCloud (ex: "Model not found")
        if resp.text:
            print(f"Détails : {resp.text}")
    except Exception as err:
        print(f"Une erreur inattendue est survenue : {err}")

if __name__ == "__main__":
    call_llm()