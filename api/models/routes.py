class Route:
    
    def __init__(self,departure, arrival, time) -> None:
        self.departure = departure
        self.arrival = arrival
        self.time = time

    def __str__(self):
        return f"<Route: {self.departure} -> {self.arrival} : {self.time}>"
