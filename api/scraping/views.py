from flask import jsonify, request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from api.models.routes import Route
from http import HTTPStatus
from api.config.config import BASE_DIR_DATA_SCRAPING_WINDOWS
from api.scraping.controllers import get_travel_time
from werkzeug.exceptions import Conflict,BadRequest


get_departure_time_arrival_namespace = Namespace("routes", description="Namespace for route times in France")

route_model = get_departure_time_arrival_namespace.model(
    'Route',{
        'departure':fields.String(required=True,description="a departure city"),
        'arrival':fields.String(required=True,description="a arrival city"),
    }
)

route_model_time = get_departure_time_arrival_namespace.model(
    'Route',{
        'departure':fields.String(required=True,description="a departure city"),
        'arrival':fields.String(required=True,description="a arrival city"),
        'time_travel':fields.String(required=True,description="travel time"),
        'time_scraping':fields.String(required=True,description="time of scraping data"),
        'file':fields.String(required=True,description="file"),
    }
)

@get_departure_time_arrival_namespace.route('/route/time')
class DepartureTimeArrival(Resource):
    @get_departure_time_arrival_namespace.doc(
        description="get travel time from a departure city to an arrival city"
    )
    @jwt_required()
    @get_departure_time_arrival_namespace.expect(route_model)
    @get_departure_time_arrival_namespace.marshal_with(route_model_time)
    def post(self):
        """
            get travel time from a departure city to an arrival city
        Args:
            departure (String): departure city
            arrival (String): arrival city
        Returns:
            time (String): travel time
        """
        data = request.get_json()

        try:

            departure = data.get('departure')
            arrival = data.get('arrival')

            get_time_travel_dpt_arr = get_travel_time(departure, arrival, BASE_DIR_DATA_SCRAPING_WINDOWS)

            if get_time_travel_dpt_arr:
                new_route = Route(
                    departure = departure,
                    arrival = arrival,
                    time_scraping = get_time_travel_dpt_arr[1],
                    time_travel = get_time_travel_dpt_arr[2],
                    file = get_time_travel_dpt_arr[0]
                )

                return new_route, HTTPStatus.CREATED
            
            else :
                response = jsonify({"error": "No data available"})
                response.status_code = 204
                return response, HTTPStatus.NO_CONTENT

        except Exception as e:
            raise Conflict(f"Exception : {e}")


   