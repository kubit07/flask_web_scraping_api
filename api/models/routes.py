import json


class Route:
    
    def __init__(self, departure, arrival, travel, time_travel):
        self.departure = departure
        self.arrival = arrival
        self.travel = travel
        self.time_travel = time_travel

    def __str__(self):
        return f"<Route: {self.departure} -> {self.arrival} : {self.time}>"
    
