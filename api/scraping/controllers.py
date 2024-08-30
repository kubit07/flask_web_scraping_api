import os
import sys 
import json
from datetime import datetime
import networkx as nx
import api.scraping.fonctionsGraphe as fg



def get_travel_time(start_city, end_city, directory):
    """
    Récupère le temps de trajet le plus récent entre `start_city` et `end_city` 
    à partir de fichiers JSON dans le répertoire spécifié.

    ### Paramètres :
    - `start_city` (str) : Ville de départ.
    - `end_city` (str) : Ville d'arrivée.
    - `directory` (str) : Chemin du répertoire contenant les fichiers JSON.

    ### Retourne :
    - `tuple` : (nom du fichier, heure de scrapping, temps de trajet entre les deux) pour 
      la paire de villes la plus récente, ou `None` si aucune correspondance n'est trouvée.
    """

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
    """
    Récupère le temps de trajet en temps réel entre `start_city` (ville de départ) et `end_city`(ville d'arrivé) 
    à partir d'un fichier JSON (données scrapées).

    La fonction lit les données du fichier JSON situé dans un sous-répertoire nommé 
    d'après le jour de la semaine courant (`day_week`) et un fichier nommé avec 
    l'heure précédente (ex: `14.json`). Elle retourne le temps de 
    trajet pour la paire de villes spécifiée, si disponible.

    ### Paramètres :
    - `start_city` (str) : Ville de départ.
    - `end_city` (str) : Ville d'arrivée.
    - `directory` (str) : Chemin du répertoire contenant les sous-répertoires des jours de la semaine.

    ### Retourne :
    - `str` : Temps de trajet pour la paire de villes si trouvée dans le fichier JSON, 
      ou `None` si aucune correspondance n'est trouvée ou si le fichier ne contient pas la clé.
    """

    now = datetime.now()
    day_week = now.strftime("%A") #permert dé récupéer le jour à partir d'une date (lundi etc.)
    hour = now.hour
    hour_file = hour-1 #car le fichier le plus récent correspond a'l'heure actuelle -1

    route_key = f"('{start_city}', '{end_city}')" 

    with open(os.path.join(f"{directory}\\{day_week}", f"{hour_file:02}.json"), 'r') as f:
            data = json.load(f)
            for travel, time in data.items():
                if (route_key == travel):
                    return time
                else:
                    None



def get_dijkstra_travel_time(start_city, end_city, directory):
    """
    Calcule le temps de trajet entre `start_city` et `end_city` en utilisant l'algorithme de Dijkstra 
    sur un graphe de routes, avec les temps de trajet chargés depuis un fichier JSON.

    ### Paramètres :
    - `start_city` (str) : Ville de départ.
    - `end_city` (str) : Ville d'arrivée.
    - `directory` (str) : Répertoire contenant les sous-répertoires des jours de la semaine avec les fichiers JSON des temps de trajet.(fichier scrapées)

    ### Retourne :
    - `tuple` : (chemin le plus court, temps total du trajet) ou `None` en cas d'erreur.

    ### Exceptions :
    - `sys.exit` : Arrête l'exécution si une arête n'est pas trouvée dans le fichier JSON.
    """
        
    # Construire le chemin complet vers le fichier JSON
    franceSimple = os.path.join(os.path.dirname(__file__), '..', 'assets', 'franceSimple.json')

    #chargement du graphe
    graphe = fg.loadGraph(franceSimple)

    now = datetime.now()
    day_week = now.strftime("%A")
    hour = now.hour
    hour_file = hour-1

    with open(os.path.join(f"{directory}\\{day_week}", f"{hour_file:02}.json"), 'r') as f:
        data = json.load(f)

    #mise à jour des attributs temps et récompense du graphe 
    for edge in graphe.edges:
        if str(edge) in data:
            graphe.edges[edge]['temps'] = data[str(edge)]
            graphe.edges[edge]['recompense'] = - data[str(edge)]
        else:
            sys.exit("Error: Edge {edge} not found in {day}.json")

    #choix de la ville de  destination
    destination = end_city

    #Choix de la ville de départ
    departure = start_city

    try:
        trajet_dijkstra = nx.dijkstra_path(graphe, departure, destination,'temps')
        trajet_dijkstra_time = nx.dijkstra_path_length(graphe,departure,destination,'temps')
        return (trajet_dijkstra, trajet_dijkstra_time)
    except:
        return None