import os
import json
from datetime import datetime

def get_travel_time(start_city, end_city, directory):
    # Lister tous les fichiers JSON dans le répertoire
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    # Trier les fichiers par date (du plus récent au plus ancien)
    files.sort(key=lambda x: datetime.strptime("_".join(x.split("_")[:-1]), "%d_%m_%Y") , reverse=True)
    
    # Parcourir les fichiers du plus récent au plus ancien
    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            data = json.load(f)
            # Chercher la clé correspondant à la paire de villes dans chaque heure de scrapping
            for hour, travels in data.items():
                route_key = f"('{start_city}', '{end_city}')"
                if route_key in travels:
                    return travels[route_key]
    
    # Si aucune correspondance n'est trouvée
    return None

# Exemple d'utilisation
start_city = "Paris"
end_city = "Lyon"
directory = "./json_files"
travel_time = get_travel_time(start_city, end_city, directory)

if travel_time:
    print(f"Le temps de trajet de {start_city} à {end_city} est {travel_time}.")
else:
    print(f"Aucun temps de trajet trouvé pour le trajet de {start_city} à {end_city}.")
