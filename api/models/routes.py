class Route:
    
    def __init__(self,departure, arrival, time_travel, time_scraping, file) -> None:
        self.departure = departure
        self.arrival = arrival
        self.time_travel = time_travel
        self.time_scraping = time_scraping
        self.file = file

    def __str__(self):
        return f"<Route: {self.departure} -> {self.arrival} : {self.time}>"
