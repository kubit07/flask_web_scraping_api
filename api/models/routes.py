import json


class Route:
    """
    Représente un itinéraire entre deux villes avec le temps de trajet.

    ### Attributs :
    - `departure` (str) : Ville de départ.
    - `arrival` (str) : Ville d'arrivée.
    - `travel` (str) : Description de l'itinéraire entre les deux villes.
    - `time_travel` (str) : Temps de trajet entre les villes.

    ### Méthodes :
    - `__init__(self, departure, arrival, travel, time_travel)` :
      Constructeur de la classe `Route`. Initialise un nouvel objet `Route` avec les informations 
      fournies sur la ville de départ, la ville d'arrivée, l'itinéraire et le temps de trajet.

    - `__str__(self)` :
      Retourne une chaîne de caractères représentant l'objet `Route` sous la forme 
      "<Route: <departure> -> <arrival> : <time_travel>>". Utilisé pour afficher une 
      représentation lisible de l'objet.
    """
    
    def __init__(self, departure, arrival, travel, time_travel):
        self.departure = departure
        self.arrival = arrival
        self.travel = travel
        self.time_travel = time_travel

    def __str__(self):
        return f"<Route: {self.departure} -> {self.arrival} : {self.time}>"
    
