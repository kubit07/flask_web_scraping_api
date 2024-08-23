import os
import json
from datetime import datetime

def get_travel_time(start_city, end_city, directory):

    results_distances = []
    results_files = []
    results = []

    route_key = f"('{start_city}', '{end_city}')" 

    # Lister tous les fichiers JSON dans le répertoire
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    # Trier les fichiers par date (du plus récent au plus ancien)
    files.sort(key=lambda x: datetime.strptime("_".join(x.split("_")[:-1]), "%d_%m_%Y") , reverse=False)
    
    # Parcourir les fichiers du plus récent au plus ancien
    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            data = json.load(f)
            # Chercher la clé correspondant à la paire de villes dans chaque heure de scrapping
            for hours, travels in data.items():
                for travel, hour in travels.items():
                    if (route_key == travel):
                        time = hour
                        results.append((file,hours,time))


    # Si aucune correspondance n'est trouvée
    return results[-1] if results else None


def get_travel_time_real_time(start_city, end_city, directory):

    now = datetime.now()
    day_week = now.strftime("%A")
    hour = now.hour
    hour_file = hour-1

    route_key = f"('{start_city}', '{end_city}')" 

    with open(os.path.join(f"{directory}\{day_week}", f"{hour_file}.json"), 'r') as f:
            data = json.load(f)
            for travel, time in data.items():
                if (route_key == travel):
                    return time
                else:
                    None



def get_dijkstra_travel_time():
    pass