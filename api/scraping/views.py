from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from api.models.routes import Route
from http import HTTPStatus

order_namespace = Namespace("routes", description="Namespace for route times in France")

@order_namespace.route('/route/<String:departure>/time/<String:arrival>')
class DepartureTimeArrival(Resource):
    @order_namespace.doc(
        description="get travel time from a departure city to an arrival city"
    )
    @jwt_required()
    def get(self):
        """
            get travel time from a departure city to an arrival city
        Args:
            departure (String): departure city
            arrival (String): arrival city
        Returns:
            time (String): travel time
        """
    
        orders= Order.query.all()

        return orders ,HTTPStatus.OK

   