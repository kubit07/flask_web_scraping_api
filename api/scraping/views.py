from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from api.models.routes import Route
from http import HTTPStatus
from api.config.config import BASE_DIR_DATA_SCRAPING_LINUX_STREAM
from api.scraping.controllers import get_dijkstra_travel_time, get_travel_time, get_travel_time_real_time
from werkzeug.exceptions import Conflict,BadRequest

# Création d'un espace de noms pour les temps de trajet entre les villes
get_departure_time_arrival_namespace = Namespace("routes", description="Namespace for route times in France")

# Définition du modèle de données pour les requêtes de temps de trajet
route_model = get_departure_time_arrival_namespace.model(
    'Route',{
        'departure':fields.String(required=True,description="a departure city"),
        'arrival':fields.String(required=True,description="a arrival city"),
    }
)

# Définition du modèle de données pour les réponses contenant les temps de trajet
route_model_time = get_departure_time_arrival_namespace.model(
    'Route',{
        'departure':fields.String(required=True,description="a departure city"),
        'arrival':fields.String(required=True,description="a arrival city"),
        'travel':fields.String(required=True,description="route from one city to another"),
        'time_travel':fields.String(required=True,description="travel time")
    }
)


@get_departure_time_arrival_namespace.route('/route/time')
class DepartureTimeArrivalRealTime(Resource):
    @get_departure_time_arrival_namespace.doc(
        description="get travel time from a departure city to an arrival city in real time"
    )
    @jwt_required()
    @get_departure_time_arrival_namespace.expect(route_model)
    @get_departure_time_arrival_namespace.marshal_with(route_model_time)
    def post(self):
        """
        pertmet d'obtenir le temps de trajet d'une ville de départ à une ville d'arrivée en temps réel
        Args:
            départ (String) : ville de départ
            arrivée (String) : ville d'arrivée
        Retours:
            time (String): temps de trajet en temps réel
        """
        data = request.get_json()

        try:
            departure = data.get('departure')
            arrival = data.get('arrival')
            time = get_travel_time_real_time(departure, arrival, BASE_DIR_DATA_SCRAPING_LINUX_STREAM)
            if time:
                new_route = Route(
                    departure = departure,
                    arrival = arrival,
                    travel = None,
                    time_travel = time
                )
                return new_route, HTTPStatus.CREATED
            
            if not time:
                get_directions_time = get_dijkstra_travel_time(departure, arrival, BASE_DIR_DATA_SCRAPING_LINUX_STREAM)
                
                if get_directions_time:
                    new_route = Route(
                        departure = departure,
                        arrival = arrival,
                        travel = get_directions_time[0],
                        time_travel = get_directions_time[1]
                    )
                    return new_route, HTTPStatus.CREATED
            
                else:
                    response = jsonify({"error": "No data available"})
                    response.status_code = 204
                    return response, HTTPStatus.NO_CONTENT

        except Exception as e:
            raise Conflict(f"Exception : {e}")


   