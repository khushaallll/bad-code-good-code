from abc import ABC, abstractmethod
from dataclasses import dataclass

# Some other function that we can't change
def fetch(lat, long):
    return {"temp_f": 71.6, "rh": 0.42, "summary": "clear"}

@dataclass
class WeatherReading:
    temperature_celsius: float
    humidity_percent: float
    description: str

# Target Interface
class WeatherClient(ABC):

    @abstractmethod
    def get_weather(self, lat: float, long: float) -> WeatherReading:
        pass

# Adapter Class
class LegacyMetClientAdapter(WeatherClient):
    def __init__(self):
        pass

    def get_weather(self, lat, long) -> WeatherReading:
        weather = fetch(lat, long)
        celsius = (weather["temp_f"] - 32) * 5/ 9
        percent = weather['rh'] * 100
        return WeatherReading(celsius, percent, weather["summary"])

        
class WeatherService:

    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client

    def get_current(self, lat: float, long: float):
        return self.weather_client.get_weather(lat, long)

weather_client = LegacyMetClientAdapter()
resp = WeatherService(weather_client).get_current(34.5, 56.7)
print(resp)